"""
Bracket Oracle — Pool Optimizer

The key insight: picking the most likely winners doesn't win pools.
You need to find spots where your edge (better predictions) meets
low ownership (what others aren't picking).

Methodology (inspired by dlm1223/march-madness):
1. Simulate tournament N times to get true win probabilities
2. Simulate opponent brackets using public pick data
3. Score all brackets against all simulations
4. Find the bracket(s) that maximize P(winning) or P(top X%)
"""

import random
from collections import defaultdict
from typing import Optional

from .models import (
    Team, Bracket, PoolConfig, SimulationResult,
    Region, Strategy, ScoringSystem,
)
from .simulator import (
    simulate_tournament, run_simulation,
    generate_bracket, simulate_game,
)


def generate_opponent_brackets(
    teams_by_region: dict[Region, list[Team]],
    public_picks: dict[str, list[float]],
    num_opponents: int = 100,
) -> list[dict[str, int]]:
    """
    Simulate opponent brackets based on public pick percentages.
    Each opponent bracket picks winners weighted by ESPN ownership.
    
    Returns list of bracket results (team_name -> furthest round).
    """
    opponents = []
    
    for _ in range(num_opponents):
        bracket_result = _generate_public_bracket(teams_by_region, public_picks)
        opponents.append(bracket_result)
    
    return opponents


def _generate_public_bracket(
    teams_by_region: dict[Region, list[Team]],
    public_picks: dict[str, list[float]],
) -> dict[str, str]:
    """
    Generate one bracket using public pick percentages as probabilities.
    Simulates how an average bracket pool participant picks.
    """
    picks = {}
    region_winners = {}
    
    for region, teams in teams_by_region.items():
        current = list(teams)
        
        for round_num in range(1, 5):
            round_idx = round_num - 1
            next_round = []
            
            for i in range(0, len(current), 2):
                a, b = current[i], current[i + 1]
                
                # Use public ownership as pick probability
                own_a = public_picks.get(a.name, [0.5] * 6)[round_idx]
                own_b = public_picks.get(b.name, [0.5] * 6)[round_idx]
                
                # Normalize
                total = own_a + own_b
                if total > 0:
                    prob_pick_a = own_a / total
                else:
                    prob_pick_a = 0.5
                
                winner = a if random.random() < prob_pick_a else b
                matchup_id = f"{region.value}_R{round_num}_{i // 2}"
                picks[matchup_id] = winner.name
                next_round.append(winner)
            
            current = next_round
        
        if current:
            region_winners[region] = current[0]
    
    # Final Four and Championship with public ownership
    regions = list(Region)
    ff_matchups = [(regions[0], regions[1]), (regions[2], regions[3])]
    ff_winners = []
    
    for r1, r2 in ff_matchups:
        if r1 in region_winners and r2 in region_winners:
            a, b = region_winners[r1], region_winners[r2]
            own_a = public_picks.get(a.name, [0.5] * 6)[4]
            own_b = public_picks.get(b.name, [0.5] * 6)[4]
            total = own_a + own_b
            prob = own_a / total if total > 0 else 0.5
            winner = a if random.random() < prob else b
            picks[f"FF_{r1.value}_{r2.value}"] = winner.name
            ff_winners.append(winner)
    
    if len(ff_winners) == 2:
        a, b = ff_winners
        own_a = public_picks.get(a.name, [0.5] * 6)[5]
        own_b = public_picks.get(b.name, [0.5] * 6)[5]
        total = own_a + own_b
        prob = own_a / total if total > 0 else 0.5
        winner = a if random.random() < prob else b
        picks["Championship"] = winner.name
    
    return picks


def score_bracket(
    bracket_picks: dict[str, str],
    actual_results: dict[str, int],
    pool_config: PoolConfig,
) -> float:
    """
    Score a bracket against actual tournament results.
    
    actual_results: team_name -> furthest round reached (1-6)
    """
    score = 0.0
    weights = pool_config.scoring_weights
    
    for matchup_id, picked_winner in bracket_picks.items():
        # Determine which round this pick is for
        round_num = _get_round_from_matchup(matchup_id)
        if round_num is None or round_num > len(weights):
            continue
        
        furthest = actual_results.get(picked_winner, 0)
        
        if furthest >= round_num:
            # Correct pick — award points
            points = weights[round_num - 1]
            
            if pool_config.scoring == ScoringSystem.SEED:
                # Seed-weighted: multiply by winning team's seed
                # (bigger upset = more points)
                # We'd need team seed lookup here
                pass
            
            score += points
    
    return score


def _get_round_from_matchup(matchup_id: str) -> Optional[int]:
    """Extract round number from matchup ID."""
    if "R1" in matchup_id:
        return 1
    elif "R2" in matchup_id:
        return 2
    elif "R3" in matchup_id:
        return 3
    elif "R4" in matchup_id:
        return 4
    elif "FF" in matchup_id:
        return 5
    elif "Championship" in matchup_id:
        return 6
    return None


def optimize_brackets(
    teams_by_region: dict[Region, list[Team]],
    pool_config: PoolConfig,
    public_picks: dict[str, list[float]],
    num_sims: int = 5000,
    num_candidate_brackets: int = 500,
    seed: Optional[int] = None,
) -> list[Bracket]:
    """
    Generate optimal bracket(s) for a pool.
    
    Algorithm:
    1. Run tournament simulation to get true win probabilities
    2. Generate candidate brackets with various strategies
    3. Generate opponent brackets using public pick data
    4. For each simulation outcome, score all brackets
    5. Return bracket(s) that maximize target percentile finish
    
    Args:
        teams_by_region: Tournament teams by region
        pool_config: Pool size, scoring, target percentile
        public_picks: ESPN/Yahoo public pick data
        num_sims: Tournament simulations to run
        num_candidate_brackets: Number of candidate brackets to evaluate
        seed: Random seed
    
    Returns:
        List of optimal brackets (pool_config.num_brackets)
    """
    if seed is not None:
        random.seed(seed)
    
    print(f"[optimizer] Running {num_sims} tournament simulations...")
    sim_result = run_simulation(teams_by_region, num_sims)
    
    # Generate candidate brackets
    print(f"[optimizer] Generating {num_candidate_brackets} candidate brackets...")
    candidates = []
    
    strategies = _get_strategies_for_pool(pool_config)
    brackets_per_strategy = num_candidate_brackets // len(strategies)
    
    for strategy in strategies:
        for _ in range(brackets_per_strategy):
            bracket = generate_bracket(
                teams_by_region, strategy, public_picks, sim_result
            )
            candidates.append(bracket)
    
    # Generate opponent brackets
    print(f"[optimizer] Simulating {pool_config.size} opponent brackets...")
    opponents = generate_opponent_brackets(
        teams_by_region, public_picks, pool_config.size
    )
    
    # Evaluate all candidates across all simulations
    print(f"[optimizer] Evaluating candidates across simulations...")
    candidate_scores = []
    
    for _ in range(num_sims):
        # Simulate one tournament outcome
        results = simulate_tournament(teams_by_region)
        
        # Score each candidate against this outcome
        sim_scores = []
        for bracket in candidates:
            my_score = score_bracket(bracket.picks, results, pool_config)
            
            # Score opponents
            opp_scores = [
                score_bracket(opp, results, pool_config)
                for opp in opponents
            ]
            opp_scores.sort()
            
            # Calculate percentile finish
            if opp_scores:
                beats = sum(1 for s in opp_scores if my_score > s)
                percentile = beats / len(opp_scores)
            else:
                percentile = 1.0
            
            sim_scores.append((my_score, percentile))
        
        candidate_scores.append(sim_scores)
    
    # Aggregate: for each candidate, calculate average percentile
    # and probability of hitting target percentile
    best_brackets = []
    
    for idx, bracket in enumerate(candidates):
        percentiles = [candidate_scores[sim][idx][1] for sim in range(len(candidate_scores))]
        avg_percentile = sum(percentiles) / len(percentiles)
        prob_target = sum(1 for p in percentiles if p >= pool_config.target_percentile) / len(percentiles)
        
        bracket.percentile = avg_percentile
        bracket.score = prob_target
        best_brackets.append((prob_target, avg_percentile, bracket))
    
    # Sort by P(target percentile), then by avg percentile
    best_brackets.sort(key=lambda x: (-x[0], -x[1]))
    
    # Return top N brackets
    result = [b for _, _, b in best_brackets[:pool_config.num_brackets]]
    
    for i, b in enumerate(result):
        print(f"[optimizer] Bracket {i + 1}: P(top {int(pool_config.target_percentile * 100)}%) = {b.score:.1%}, avg percentile = {b.percentile:.1%}")
    
    return result


def _get_strategies_for_pool(pool_config: PoolConfig) -> list[Strategy]:
    """
    Select bracket strategies based on pool size.
    Small pools → more chalk. Large pools → more contrarian/chaos.
    """
    size = pool_config.size
    
    if size <= 10:
        return [Strategy.CHALK, Strategy.BALANCED]
    elif size <= 50:
        return [Strategy.CHALK, Strategy.BALANCED, Strategy.CONTRARIAN]
    elif size <= 200:
        return [Strategy.BALANCED, Strategy.CONTRARIAN, Strategy.CHAOS]
    else:
        # Mega pool — need differentiation
        return [Strategy.CONTRARIAN, Strategy.CHAOS]


def quick_value_analysis(
    sim_result: SimulationResult,
    public_picks: dict[str, list[float]],
    top_n: int = 20,
) -> list[dict]:
    """
    Quick analysis: find the most undervalued and overvalued teams.
    
    Value = win probability - ownership percentage
    Positive = underowned (good contrarian pick)
    Negative = overowned (avoid)
    """
    analysis = []
    
    for team_name, probs in sim_result.round_probs.items():
        if team_name not in public_picks:
            continue
        
        ownership = public_picks[team_name]
        
        # Focus on championship round for biggest impact
        for round_idx in range(min(len(probs), len(ownership))):
            round_names = ["R64", "R32", "S16", "E8", "F4", "Champ"]
            value = probs[round_idx] - ownership[round_idx]
            
            if round_idx >= 3:  # Only report E8+ for clarity
                analysis.append({
                    "team": team_name,
                    "round": round_names[round_idx],
                    "win_prob": probs[round_idx],
                    "ownership": ownership[round_idx],
                    "value": value,
                    "verdict": "UNDEROWNED 🎯" if value > 0.05 else ("OVEROWNED ⚠️" if value < -0.05 else "FAIR"),
                })
    
    # Sort by absolute value (most mispriced first)
    analysis.sort(key=lambda x: -abs(x["value"]))
    return analysis[:top_n]
