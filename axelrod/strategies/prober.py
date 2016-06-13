from axelrod import Actions, Player, init_args, random_choice

C, D = Actions.C, Actions.D


class Prober(Player):
    """
    Plays D, C, C initially. Defects forever if opponent cooperated in moves 2
    and 3. Otherwise plays TFT.
    """

    name = 'Prober'
    classifier = {
        'stochastic': False,
        'memory_depth': float('inf'),  # Long memory
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        turn = len(self.history)
        if turn == 0:
            return D
        if turn == 1:
            return C
        if turn == 2:
            return C
        if turn > 2:
            if opponent.history[1: 3] == [C, C]:
                return D
            else:
                # TFT
                return D if opponent.history[-1:] == [D] else C


class Prober2(Player):
    """
    Plays D, C, C initially. Cooperates forever if opponent played D then C
    in moves 2 and 3. Otherwise plays TFT.
    """

    name = 'Prober 2'
    classifier = {
        'stochastic': False,
        'memory_depth': float('inf'),  # Long memory
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        turn = len(self.history)
        if turn == 0:
            return D
        if turn == 1:
            return C
        if turn == 2:
            return C
        if turn > 2:
            if opponent.history[1: 3] == [D, C]:
                return C
            else:
                # TFT
                return D if opponent.history[-1:] == [D] else C


class Prober3(Player):
    """
    Plays D, C initially. Defects forever if opponent played C in moves 2.
    Otherwise plays TFT.
    """

    name = 'Prober 3'
    classifier = {
        'stochastic': False,
        'memory_depth': float('inf'),  # Long memory
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        turn = len(self.history)
        if turn == 0:
            return D
        if turn == 1:
            return C
        if turn > 1:
            if opponent.history[1] == C:
                return D
            else:
                # TFT
                return D if opponent.history[-1:] == [D] else C


class HardProber(Player):
    """
    Plays D, D, C, C initially. Defects forever if opponent cooperated in moves
    2 and 3. Otherwise plays TFT.
    """

    name = 'Hard Prober'
    classifier = {
        'stochastic': False,
        'memory_depth': float('inf'),  # Long memory
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        turn = len(self.history)
        if turn == 0:
            return D
        if turn == 1:
            return D
        if turn == 2:
            return C
        if turn == 3:
            return C
        if turn > 3:
            if opponent.history[1: 3] == [C, C]:
                return D
            else:
                # TFT
                return D if opponent.history[-1:] == [D] else C


class NaiveProber(Player):
    """
    Like tit-for-tat, but it occasionally defects with a small probability.
    """

    name = 'Naive Prober'
    classifier = {
        'memory_depth': 1,  # Four-Vector = (1.,0.,1.,0.)
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @init_args
    def __init__(self, p=0.1):
        """
        Parameters
        ----------
        p, float
            The probability to defect randomly
        """
        Player.__init__(self)
        self.p = p
        if (self.p == 0) or (self.p == 1):
            self.classifier['stochastic'] = False

    def strategy(self, opponent):
        # First move
        if len(self.history) == 0:
            return C
        # React to the opponent's last move
        if opponent.history[-1] == D:
            return D
        # Otherwise cooperate, defect with a small probability
        choice = random_choice(1 - self.p)
        return choice

    def __repr__(self):
        return "%s: %s" % (self.name, round(self.p, 2))
