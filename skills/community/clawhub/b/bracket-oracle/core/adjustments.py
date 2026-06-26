"""
Bracket Oracle — Team Adjustments (Public)

Basic tournament-weighted composite scoring using Torvik data.
Combines efficiency metrics with historical calibration weights.
"""

import json
from pathlib import Path
from .data import fetch_torvik_ratings, DATA_DIR


def generate_adjusted_rankings(year: int = 2026, top_n: int = 68) -> list[dict]:
    """
    Generate tournament-adjusted rankings from Torvik data.
    
    Uses a weighted composite of efficiency metrics calibrated
    against historical tournament outcomes (2015-2025).
    
    Weights derived from factor analysis:
        - AdjEM (net efficiency margin): primary signal
        - Barthag (win probability vs avg team): secondary
        - AdjOE (offense): tertiary
        - AdjDE (defense): supporting
    
    Returns sorted list of team dicts with adjusted scores.
    """
    teams = fetch_torvik_ratings(year)
    if not teams:
        return []
    
    results = []
    for t in teams:
        try:
            rank = int(t.get("rank", 999))
            adj_oe = float(t.get("adj_oe", 0))
            adj_de = float(t.get("adj_de", 0))
            barthag = float(t.get("barthag", 0))
            adj_em = float(t.get("adj_em", adj_oe - adj_de))
            
            # Tournament-weighted composite
            # Historically: AdjEM ~23%, Barthag ~17%, AdjOE ~17%, AdjDE ~14%
            composite = (
                adj_em * 0.45 +          # Net efficiency (dominant predictor)
                barthag * 30.0 * 0.25 +   # Win prob scaled to ~same range
                adj_oe * 0.18 +           # Offense (slightly > defense in March)
                (100 - adj_de) * 0.12     # Defense (inverted, lower = better)
            )
            
            results.append({
                "team": t["team"],
                "conf": t.get("conf", ""),
                "record": t.get("record", ""),
                "torvik_rank": rank,
                "adj_em": adj_em,
                "adj_oe": adj_oe,
                "adj_de": adj_de,
                "barthag": barthag,
                "composite_score": composite,
                "adjusted_score": composite,  # No additional adjustments in public version
            })
        except (ValueError, TypeError, KeyError):
            continue
    
    # Sort by adjusted score
    results.sort(key=lambda x: -x["adjusted_score"])
    
    # Assign adjusted ranks
    for i, r in enumerate(results):
        r["adjusted_rank"] = i + 1
        r["rank_change"] = r["torvik_rank"] - (i + 1)
    
    return results[:top_n]
