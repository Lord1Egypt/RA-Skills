"""
Bracket Oracle — Monte Carlo Tournament Simulator

Simulates the NCAA tournament N times to produce round-by-round
probabilities for every team.
"""

import random
from collections import defaultdict
from typing import Optional

from .models import (
    Team, Matchup, Bracket, SimulationResult,
    Region, Strategy, seed_win_probability,
)


def simulate_game(team_a: Team, team_b: Team, use_ratings: bool = True) -> Team:
    """
    Simulate a single game between two teams.
    Returns the winner based on probabilistic outcome.
    """
    if use_ratings and team_a.ratings and team_b.ratings:
        prob_a = team_a.win_probability(team_b)
    else:
        prob_a = seed_win_probability(team_a.seed, team_b.seed)
    
    return team_a if random.random() < prob_a else team_b


def simulate_region(teams: list[Team], region: Region) -> list[list[Team]]:
    """
    Simulate a single region (16 teams) through 4 rounds.
    Returns list of round results (winners per round).
    
    Teams should be in bracket order:
    [1-seed, 16-seed, 8-seed, 9-seed, 5-seed, 12-seed, 4-seed, 13-seed,
     6-seed, 11-seed, 3-seed, 14-seed, 7-seed, 10-seed, 2-seed, 15-seed]
    """
    rounds = []
    current = list(teams)
    
    for round_num in range(4):  # R64, R32, S16, E8
        next_round = []
        for i in range(0, len(current), 2):
            winner = simulate_game(current[i], current[i + 1])
            next_round.append(winner)
        rounds.append(next_round)
        current = next_round
    
    return rounds


def simulate_tournament(teams_by_region: dict[Region, list[Team]]) -> dict[str, int]:
    """
    Simulate one full tournament.
    Returns dict of team_name -> furthest round reached (1-6).
    """
    results = defaultdict(int)
    
    # Track all teams — they all made at least round 1
    for region_teams in teams_by_region.values():
        for team in region_teams:
            results[team.name] = 0  # Will be updated
    
    # Simulate each region
    region_winners = {}
    for region, teams in teams_by_region.items():
        rounds = simulate_region(teams, region)
        
        # Record results per round
        for round_idx, round_winners in enumerate(rounds):
            round_num = round_idx + 1  # 1-4
            for team in round_winners:
                results[team.name] = max(results[team.name], round_num)
        
        region_winners[region] = rounds[-1][0]  # E8 winner = region winner
    
    # Final Four
    regions = list(Region)
    # Standard FF matchups: South vs East, West vs Midwest
    ff_matchups = [
        (regions[0], regions[1]),  # South vs East
        (regions[2], regions[3]),  # West vs Midwest
    ]
    
    ff_winners = []
    for r1, r2 in ff_matchups:
        if r1 in region_winners and r2 in region_winners:
            winner = simulate_game(region_winners[r1], region_winners[r2])
            results[winner.name] = max(results[winner.name], 5)  # Final Four
            ff_winners.append(winner)
    
    # Championship
    if len(ff_winners) == 2:
        champion = simulate_game(ff_winners[0], ff_winners[1])
        results[champion.name] = 6  # Champion
    
    return dict(results)


def run_simulation(
    teams_by_region: dict[Region, list[Team]],
    num_sims: int = 10000,
    seed: Optional[int] = None,
) -> SimulationResult:
    """
    Run Monte Carlo tournament simulation.
    
    Args:
        teams_by_region: Dict mapping Region -> list of 16 teams in bracket order
        num_sims: Number of simulations to run
        seed: Random seed for reproducibility
    
    Returns:
        SimulationResult with round probabilities for all teams
    """
    if seed is not None:
        random.seed(seed)
    
    # Track how many times each team reaches each round
    round_counts = defaultdict(lambda: [0] * 6)  # team -> [R1, R2, R3, R4, F4, Champ]
    
    for _ in range(num_sims):
        results = simulate_tournament(teams_by_region)
        
        for team_name, furthest_round in results.items():
            for r in range(furthest_round):
                round_counts[team_name][r] += 1
    
    # Convert counts to probabilities
    round_probs = {}
    championship_probs = {}
    
    for team_name, counts in round_counts.items():
        probs = [c / num_sims for c in counts]
        round_probs[team_name] = probs
        championship_probs[team_name] = probs[5] if len(probs) > 5 else 0.0
    
    # Find most likely Final Four and champion
    sorted_champ = sorted(championship_probs.items(), key=lambda x: -x[1])
    most_likely_champion = sorted_champ[0][0] if sorted_champ else ""
    
    # F4 = teams with highest P(reaching round 5)
    f4_probs = [(name, probs[4]) for name, probs in round_probs.items()]
    f4_sorted = sorted(f4_probs, key=lambda x: -x[1])
    most_likely_f4 = [name for name, _ in f4_sorted[:4]]
    
    return SimulationResult(
        num_sims=num_sims,
        round_probs=round_probs,
        championship_probs=championship_probs,
        most_likely_f4=most_likely_f4,
        most_likely_champion=most_likely_champion,
    )


def generate_bracket(
    teams_by_region: dict[Region, list[Team]],
    strategy: Strategy = Strategy.BALANCED,
    public_picks: Optional[dict[str, list[float]]] = None,
    sim_result: Optional[SimulationResult] = None,
) -> Bracket:
    """
    Generate a complete bracket using the specified strategy.

    Strategies:
        CHALK: Always pick the team with higher win probability
        CONTRARIAN: Pick undervalued teams (high prob, low ownership)
        BALANCED: Mix chalk early rounds, contrarian late rounds
        CHAOS: Maximum upset potential

    Returns picks for all 63 games including Final Four and Championship.
    """
    all_teams = []
    picks = {}
    region_winners = {}

    for region, teams in teams_by_region.items():
        all_teams.extend(teams)
        current = list(teams)

        for round_num in range(1, 5):  # R64 through E8
            next_round = []
            for i in range(0, len(current), 2):
                a, b = current[i], current[i + 1]
                winner = _pick_winner(a, b, round_num, strategy, public_picks, sim_result)
                matchup_id = f"{region.value}_R{round_num}_{i // 2}"
                picks[matchup_id] = winner.name
                next_round.append(winner)
            current = next_round

        if current:
            region_winners[region] = current[0]

    ff_matchups = [
        (Region.SOUTH, Region.EAST),
        (Region.WEST, Region.MIDWEST),
    ]
    ff_winners = []

    for r1, r2 in ff_matchups:
        if r1 in region_winners and r2 in region_winners:
            a, b = region_winners[r1], region_winners[r2]
            winner = _pick_winner(a, b, 5, strategy, public_picks, sim_result)
            picks[f"FF_{r1.value}_{r2.value}"] = winner.name
            ff_winners.append(winner)

    if len(ff_winners) == 2:
        a, b = ff_winners
        winner = _pick_winner(a, b, 6, strategy, public_picks, sim_result)
        picks["Championship"] = winner.name

    return Bracket(teams=all_teams, picks=picks, strategy=strategy)


def _pick_winner(
    team_a: Team,
    team_b: Team,
    round_num: int,
    strategy: Strategy,
    public_picks: Optional[dict[str, list[float]]],
    sim_result: Optional[SimulationResult],
) -> Team:
    """Pick a winner based on strategy."""
    
    prob_a = team_a.win_probability(team_b)
    
    if strategy == Strategy.CHALK:
        return team_a if prob_a >= 0.5 else team_b
    
    elif strategy == Strategy.CHAOS:
        # Favor the underdog, weighted by upset probability
        upset_bonus = 0.20  # Shift probability toward underdog
        adjusted = prob_a - upset_bonus if prob_a > 0.5 else prob_a + upset_bonus
        return team_a if random.random() < adjusted else team_b
    
    elif strategy == Strategy.CONTRARIAN:
        return _contrarian_pick(team_a, team_b, round_num, prob_a, public_picks, sim_result)
    
    elif strategy == Strategy.BALANCED:
        # Chalk in early rounds, contrarian in later rounds
        if round_num <= 2:
            return team_a if prob_a >= 0.5 else team_b
        else:
            return _contrarian_pick(team_a, team_b, round_num, prob_a, public_picks, sim_result)
    
    # Default: probability-based
    return team_a if random.random() < prob_a else team_b


def _contrarian_pick(
    team_a: Team,
    team_b: Team,
    round_num: int,
    prob_a: float,
    public_picks: Optional[dict[str, list[float]]],
    sim_result: Optional[SimulationResult],
) -> Team:
    """
    Make a contrarian pick — find value where win probability
    exceeds public ownership.
    """
    if not public_picks:
        # No public data — use mild upset bias
        if prob_a > 0.5:
            # Slight chance to pick the underdog
            return team_b if random.random() < 0.25 else team_a
        else:
            return team_a if random.random() < 0.25 else team_b
    
    round_idx = round_num - 1
    
    own_a = public_picks.get(team_a.name, [0.5] * 6)[round_idx]
    own_b = public_picks.get(team_b.name, [0.5] * 6)[round_idx]
    
    # Value = win probability - ownership (positive = underowned)
    value_a = prob_a - own_a
    value_b = (1.0 - prob_a) - own_b
    
    # Late rounds matter more — amplify contrarian edge
    leverage = 1.0 + (round_num - 1) * 0.3
    
    score_a = prob_a + (value_a * leverage * 0.5)
    score_b = (1.0 - prob_a) + (value_b * leverage * 0.5)
    
    return team_a if score_a >= score_b else team_b
