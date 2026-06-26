"""
Bracket Oracle — Data Models

Core data structures for teams, matchups, brackets, and pools.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Region(Enum):
    SOUTH = "South"
    EAST = "East"
    WEST = "West"
    MIDWEST = "Midwest"


class Strategy(Enum):
    CHALK = "chalk"           # Favor higher seeds / higher ratings
    CONTRARIAN = "contrarian" # Favor undervalued teams (low ownership, decent win prob)
    BALANCED = "balanced"     # Mix of chalk and contrarian
    CHAOS = "chaos"           # Maximum upset potential for mega pools
    CUSTOM = "custom"         # User-defined weights


class ScoringSystem(Enum):
    STANDARD = "standard"     # 1-2-4-8-16-32 (ESPN default)
    UPSET = "upset"           # Bonus points for picking upsets
    SEED = "seed"             # Points = seed of winning team
    CUSTOM = "custom"


@dataclass
class TeamRatings:
    """Adjusted efficiency metrics from KenPom or Torvik."""
    adj_em: float              # Adjusted Efficiency Margin (net)
    adj_o: float               # Adjusted Offensive Efficiency
    adj_d: float               # Adjusted Defensive Efficiency
    adj_tempo: float           # Adjusted Tempo
    sos: Optional[float] = None           # Strength of Schedule
    sos_adj_em: Optional[float] = None    # SOS by adj efficiency margin
    luck: Optional[float] = None          # Luck rating
    source: str = "torvik"     # "torvik" or "kenpom"


@dataclass
class Team:
    """A tournament team with seed, ratings, and metadata."""
    name: str
    seed: int
    region: Region
    conference: str = ""
    record: str = ""
    ratings: Optional[TeamRatings] = None
    # Public pick percentages by round (R1 through R6/championship)
    public_picks: list[float] = field(default_factory=lambda: [0.0] * 6)

    @property
    def adj_em(self) -> float:
        return self.ratings.adj_em if self.ratings else 0.0

    def win_probability(self, opponent: "Team") -> float:
        """
        Calculate win probability against opponent using log5 method
        with adjusted efficiency margin.

        Uses the Pythagorean expectation adapted for tempo-free stats.
        """
        if not self.ratings or not opponent.ratings:
            # Fallback to seed-based probability
            return seed_win_probability(self.seed, opponent.seed)

        # Log5 with adjusted EM
        # Probability = 1 / (1 + 10^((opp_em - team_em) * k))
        # k calibrated to historical NCAA tournament data
        k = 0.0325  # Calibration constant
        em_diff = self.ratings.adj_em - opponent.ratings.adj_em
        prob = 1.0 / (1.0 + 10 ** (-em_diff * k))
        return max(0.01, min(0.99, prob))


@dataclass
class Matchup:
    """A single game between two teams."""
    team_a: Team
    team_b: Team
    round_num: int  # 1=R64, 2=R32, 3=S16, 4=E8, 5=F4, 6=Championship
    region: Optional[Region] = None
    winner: Optional[Team] = None


@dataclass
class Bracket:
    """A complete 64-team bracket with picks for all rounds."""
    teams: list[Team]                    # 64 teams in bracket order
    picks: dict[str, str] = field(default_factory=dict)  # matchup_id -> winner_name
    strategy: Strategy = Strategy.BALANCED
    score: float = 0.0
    percentile: float = 0.0

    def to_dict(self) -> dict:
        return {
            "teams": [t.name for t in self.teams],
            "picks": self.picks,
            "strategy": self.strategy.value,
            "score": self.score,
            "percentile": self.percentile,
        }


@dataclass
class PoolConfig:
    """Configuration for a bracket pool."""
    name: str
    size: int                            # Number of participants
    scoring: ScoringSystem = ScoringSystem.STANDARD
    custom_scoring: Optional[list[int]] = None  # Points per round if custom
    num_brackets: int = 1                # How many brackets to generate
    target_percentile: float = 0.90      # Target finish percentile

    @property
    def scoring_weights(self) -> list[int]:
        if self.scoring == ScoringSystem.STANDARD:
            return [1, 2, 4, 8, 16, 32]
        elif self.scoring == ScoringSystem.UPSET:
            return [1, 2, 4, 8, 16, 32]  # Plus seed bonus
        elif self.scoring == ScoringSystem.SEED:
            return [1, 1, 1, 1, 1, 1]  # Multiplied by seed
        elif self.custom_scoring:
            return self.custom_scoring
        return [1, 2, 4, 8, 16, 32]


@dataclass
class SimulationResult:
    """Results from a Monte Carlo tournament simulation."""
    num_sims: int
    # team_name -> [P(R1), P(R2), ..., P(Championship)]
    round_probs: dict[str, list[float]] = field(default_factory=dict)
    # team_name -> P(winning it all)
    championship_probs: dict[str, float] = field(default_factory=dict)
    # Most likely Final Four
    most_likely_f4: list[str] = field(default_factory=list)
    # Most likely champion
    most_likely_champion: str = ""


def seed_win_probability(seed_a: int, seed_b: int) -> float:
    """
    Historical seed-based win probability for NCAA tournament.
    Based on all tournament games 1985-2024.
    """
    # Historical upset rates by seed matchup (approximate)
    historical = {
        (1, 16): 0.99, (2, 15): 0.94, (3, 14): 0.85, (4, 13): 0.79,
        (5, 12): 0.65, (6, 11): 0.63, (7, 10): 0.61, (8, 9): 0.51,
        # Later rounds use seed differential
    }

    if seed_a > seed_b:
        key = (seed_b, seed_a)
        if key in historical:
            return 1.0 - historical[key]
    else:
        key = (seed_a, seed_b)
        if key in historical:
            return historical[key]

    # Generic model for non-standard matchups
    diff = seed_b - seed_a  # Positive means team_a is better seed
    prob = 1.0 / (1.0 + 10 ** (-diff * 0.06))
    return max(0.01, min(0.99, prob))
