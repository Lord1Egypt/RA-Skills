"""
Bracket Oracle — Historical Calibration

Cross-reference Torvik T-Rank against actual tournament results
to calibrate win probability model and identify which metrics
best predict March Madness success.

Key questions:
1. How well does Torvik AdjEM predict tournament wins?
2. Does Torvik systematically over/underrate certain team profiles?
3. Which four factors best predict tournament success?
4. How do Torvik rankings compare to KenPom historically?
"""

import json
import math
import os
import requests
from collections import defaultdict
from pathlib import Path
from typing import Optional

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

TORVIK_JSON_URL = "https://barttorvik.com/{year}_team_results.json"

# Historical tournament results (champion + Final Four)
# Source: NCAA records
TOURNAMENT_RESULTS = {
    2015: {
        "champion": "Duke",
        "runner_up": "Wisconsin",
        "final_four": ["Duke", "Wisconsin", "Michigan St.", "Kentucky"],
        "cinderellas": ["UCLA"],  # 11-seed E8
    },
    2016: {
        "champion": "Villanova",
        "runner_up": "North Carolina",
        "final_four": ["Villanova", "North Carolina", "Oklahoma", "Syracuse"],
        "cinderellas": ["Syracuse"],  # 10-seed F4
    },
    2017: {
        "champion": "North Carolina",
        "runner_up": "Gonzaga",
        "final_four": ["North Carolina", "Gonzaga", "Oregon", "South Carolina"],
        "cinderellas": ["South Carolina"],  # 7-seed F4
    },
    2018: {
        "champion": "Villanova",
        "runner_up": "Michigan",
        "final_four": ["Villanova", "Michigan", "Kansas", "Loyola Chicago"],
        "cinderellas": ["Loyola Chicago"],  # 11-seed F4
    },
    2019: {
        "champion": "Virginia",
        "runner_up": "Texas Tech",
        "final_four": ["Virginia", "Texas Tech", "Michigan St.", "Auburn"],
        "cinderellas": ["Auburn"],  # 5-seed F4 (mild)
    },
    # 2020: No tournament (COVID)
    2021: {
        "champion": "Baylor",
        "runner_up": "Gonzaga",
        "final_four": ["Baylor", "Gonzaga", "Houston", "UCLA"],
        "cinderellas": ["UCLA"],  # 11-seed F4
    },
    2022: {
        "champion": "Kansas",
        "runner_up": "North Carolina",
        "final_four": ["Kansas", "North Carolina", "Villanova", "Duke"],
        "cinderellas": ["North Carolina"],  # 8-seed runner-up
    },
    2023: {
        "champion": "Connecticut",
        "runner_up": "San Diego St.",
        "final_four": ["Connecticut", "San Diego St.", "Miami FL", "Florida Atlantic"],
        "cinderellas": ["Florida Atlantic"],  # 9-seed F4
    },
    2024: {
        "champion": "Connecticut",
        "runner_up": "Purdue",
        "final_four": ["Connecticut", "Purdue", "Alabama", "NC State"],
        "cinderellas": ["NC State"],  # 11-seed F4
    },
    2025: {
        "champion": "Florida",
        "runner_up": "Houston",
        "final_four": ["Florida", "Houston", "Auburn", "Duke"],
        "cinderellas": [],
    },
}


def fetch_historical_torvik(years: Optional[list[int]] = None, force: bool = False) -> dict[int, list]:
    """Fetch Torvik data for multiple years."""
    if years is None:
        years = list(TOURNAMENT_RESULTS.keys())
    
    all_data = {}
    headers = {"User-Agent": "Mozilla/5.0 (compatible; BracketOracle/1.0)"}
    
    for year in years:
        cache_file = DATA_DIR / f"torvik_{year}.json"
        
        if cache_file.exists() and not force:
            with open(cache_file) as f:
                all_data[year] = json.load(f)
            print(f"  {year}: loaded from cache ({len(all_data[year])} teams)")
            continue
        
        try:
            url = TORVIK_JSON_URL.format(year=year)
            r = requests.get(url, headers=headers, timeout=15)
            r.raise_for_status()
            raw = json.loads(r.text)
            
            # Parse into dicts
            from .data import _parse_torvik_json
            teams = _parse_torvik_json(raw)
            
            with open(cache_file, "w") as f:
                json.dump(teams, f, indent=2)
            
            all_data[year] = teams
            print(f"  {year}: fetched {len(teams)} teams")
        except Exception as e:
            print(f"  {year}: ERROR - {e}")
    
    return all_data


def analyze_champion_profile(historical_data: dict[int, list]) -> dict:
    """
    Analyze the statistical profile of tournament champions.
    What do champions look like in Torvik data?
    """
    profiles = []
    
    for year, results in TOURNAMENT_RESULTS.items():
        if year not in historical_data:
            continue
        
        champ_name = results["champion"]
        teams = historical_data[year]
        
        champ = None
        for t in teams:
            if t.get("team") == champ_name:
                champ = t
                break
        
        if not champ:
            # Try fuzzy match
            for t in teams:
                if champ_name.lower() in t.get("team", "").lower():
                    champ = t
                    break
        
        if champ:
            profiles.append({
                "year": year,
                "team": champ.get("team"),
                "rank": champ.get("rank"),
                "adj_em": champ.get("adj_em", 0),
                "adj_oe": champ.get("adj_oe", 0),
                "adj_de": champ.get("adj_de", 0),
                "barthag": champ.get("barthag", 0),
                "efg_o": champ.get("efg_o", 0),
                "to_o": champ.get("to_o", 0),
                "or_pct": champ.get("or_pct", 0),
                "efg_d": champ.get("efg_d", 0),
            })
    
    if not profiles:
        return {"error": "No champion data found"}
    
    # Compute averages and ranges
    metrics = ["rank", "adj_em", "adj_oe", "adj_de", "barthag", "efg_o", "to_o", "or_pct", "efg_d"]
    summary = {}
    
    for m in metrics:
        values = [p[m] for p in profiles if p.get(m)]
        if values:
            summary[m] = {
                "mean": sum(values) / len(values),
                "min": min(values),
                "max": max(values),
                "values": {p["year"]: p[m] for p in profiles if p.get(m)},
            }
    
    return {
        "champions": profiles,
        "summary": summary,
        "n": len(profiles),
    }


def analyze_final_four_profile(historical_data: dict[int, list]) -> dict:
    """Analyze what Final Four teams look like statistically."""
    all_f4 = []
    
    for year, results in TOURNAMENT_RESULTS.items():
        if year not in historical_data:
            continue
        
        teams = historical_data[year]
        team_lookup = {t.get("team", ""): t for t in teams}
        
        for f4_team in results["final_four"]:
            t = team_lookup.get(f4_team)
            if not t:
                # Fuzzy
                for name, data in team_lookup.items():
                    if f4_team.lower() in name.lower():
                        t = data
                        break
            
            if t:
                all_f4.append({
                    "year": year,
                    "team": t.get("team"),
                    "rank": t.get("rank"),
                    "adj_em": t.get("adj_em", 0),
                    "barthag": t.get("barthag", 0),
                })
    
    if not all_f4:
        return {"error": "No F4 data found"}
    
    ranks = [t["rank"] for t in all_f4 if t.get("rank")]
    adj_ems = [t["adj_em"] for t in all_f4 if t.get("adj_em")]
    
    return {
        "total_f4_teams": len(all_f4),
        "rank_stats": {
            "mean": sum(ranks) / len(ranks) if ranks else 0,
            "median": sorted(ranks)[len(ranks) // 2] if ranks else 0,
            "min": min(ranks) if ranks else 0,
            "max": max(ranks) if ranks else 0,
            "pct_top_10": sum(1 for r in ranks if r <= 10) / len(ranks) if ranks else 0,
            "pct_top_25": sum(1 for r in ranks if r <= 25) / len(ranks) if ranks else 0,
        },
        "adj_em_stats": {
            "mean": sum(adj_ems) / len(adj_ems) if adj_ems else 0,
            "min": min(adj_ems) if adj_ems else 0,
            "max": max(adj_ems) if adj_ems else 0,
        },
        "teams": all_f4,
    }


def calibrate_win_probability(historical_data: dict[int, list]) -> dict:
    """
    Compare Torvik-predicted win probability (barthag) against 
    actual tournament performance to find calibration offsets.
    
    Key insight: Torvik barthag is win% vs average D1 team.
    Tournament fields are NOT average D1 — they're the top ~20%.
    So we need to adjust.
    """
    # Group teams by Torvik rank bucket and check actual tournament performance
    rank_buckets = {
        "1-5": {"predicted_f4": 0, "actual_f4": 0, "predicted_champ": 0, "actual_champ": 0, "n": 0},
        "6-15": {"predicted_f4": 0, "actual_f4": 0, "predicted_champ": 0, "actual_champ": 0, "n": 0},
        "16-30": {"predicted_f4": 0, "actual_f4": 0, "predicted_champ": 0, "actual_champ": 0, "n": 0},
        "31-50": {"predicted_f4": 0, "actual_f4": 0, "predicted_champ": 0, "actual_champ": 0, "n": 0},
        "51+": {"predicted_f4": 0, "actual_f4": 0, "predicted_champ": 0, "actual_champ": 0, "n": 0},
    }
    
    for year, results in TOURNAMENT_RESULTS.items():
        if year not in historical_data:
            continue
        
        teams = historical_data[year]
        team_lookup = {t.get("team", ""): t for t in teams}
        
        f4_set = set(results["final_four"])
        champ = results["champion"]
        
        for t in teams:
            rank = t.get("rank", 999)
            name = t.get("team", "")
            
            if rank <= 5:
                bucket = "1-5"
            elif rank <= 15:
                bucket = "6-15"
            elif rank <= 30:
                bucket = "16-30"
            elif rank <= 50:
                bucket = "31-50"
            else:
                continue  # Skip teams unlikely to be in tournament
            
            rank_buckets[bucket]["n"] += 1
            
            if name in f4_set:
                rank_buckets[bucket]["actual_f4"] += 1
            if name == champ:
                rank_buckets[bucket]["actual_champ"] += 1
    
    # Calculate rates
    for bucket, data in rank_buckets.items():
        if data["n"] > 0:
            data["f4_rate"] = data["actual_f4"] / data["n"]
            data["champ_rate"] = data["actual_champ"] / data["n"]
        else:
            data["f4_rate"] = 0
            data["champ_rate"] = 0
    
    return rank_buckets


def compute_prediction_accuracy(historical_data: dict[int, list]) -> dict:
    """
    For each year, check: if we picked the top-N Torvik teams,
    how many actual Final Four teams would we have gotten?
    """
    accuracy = {}
    
    for year, results in TOURNAMENT_RESULTS.items():
        if year not in historical_data:
            continue
        
        teams = historical_data[year]
        f4_set = set(results["final_four"])
        champ = results["champion"]
        
        # Sort by rank
        sorted_teams = sorted(teams, key=lambda t: t.get("rank", 999))
        top_names = [t.get("team") for t in sorted_teams]
        
        # How many F4 teams in top N?
        for n in [4, 8, 16, 25]:
            top_n = set(top_names[:n])
            hits = len(f4_set & top_n)
            if year not in accuracy:
                accuracy[year] = {"champion": champ, "champ_rank": None}
            accuracy[year][f"f4_in_top_{n}"] = hits
        
        # What was the champion's Torvik rank?
        for t in sorted_teams:
            if t.get("team") == champ:
                accuracy[year]["champ_rank"] = t.get("rank")
                break
    
    return accuracy


def run_full_calibration(force_fetch: bool = False) -> dict:
    """
    Run complete historical calibration analysis.
    Returns comprehensive results for tuning the model.
    """
    print("=== Bracket Oracle Historical Calibration ===\n")
    
    print("1. Fetching historical Torvik data...")
    historical = fetch_historical_torvik(force=force_fetch)
    
    print(f"\n2. Analyzing champion profiles ({len(TOURNAMENT_RESULTS)} tournaments)...")
    champ_profile = analyze_champion_profile(historical)
    
    print("3. Analyzing Final Four profiles...")
    f4_profile = analyze_final_four_profile(historical)
    
    print("4. Calibrating win probability by rank bucket...")
    calibration = calibrate_win_probability(historical)
    
    print("5. Computing prediction accuracy...")
    accuracy = compute_prediction_accuracy(historical)
    
    # Summary
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    
    if "summary" in champ_profile:
        rank_data = champ_profile["summary"].get("rank", {})
        em_data = champ_profile["summary"].get("adj_em", {})
        print(f"\nChampion Profile (n={champ_profile['n']}):")
        print(f"  Torvik Rank: mean={rank_data.get('mean', 0):.1f}, range={rank_data.get('min', 0)}-{rank_data.get('max', 0)}")
        print(f"  AdjEM: mean={em_data.get('mean', 0):.1f}, range={em_data.get('min', 0):.1f}-{em_data.get('max', 0):.1f}")
    
    if "rank_stats" in f4_profile:
        rs = f4_profile["rank_stats"]
        print(f"\nFinal Four Profile (n={f4_profile['total_f4_teams']}):")
        print(f"  Torvik Rank: mean={rs['mean']:.1f}, median={rs['median']}")
        print(f"  % in Top 10: {rs['pct_top_10']:.0%}")
        print(f"  % in Top 25: {rs['pct_top_25']:.0%}")
    
    print(f"\nPrediction Accuracy by Year:")
    for year, acc in sorted(accuracy.items()):
        print(f"  {year}: Champ={acc['champion']} (rank #{acc.get('champ_rank', '?')}), "
              f"F4 in top 4: {acc.get('f4_in_top_4', '?')}/4, "
              f"F4 in top 16: {acc.get('f4_in_top_16', '?')}/4")
    
    print(f"\nCalibration by Rank Bucket:")
    for bucket, data in calibration.items():
        if data["n"] > 0:
            print(f"  {bucket:>5}: F4 rate={data['f4_rate']:.1%} ({data['actual_f4']}/{data['n']}), "
                  f"Champ rate={data['champ_rate']:.1%}")
    
    # Save results
    results = {
        "champion_profile": champ_profile,
        "final_four_profile": f4_profile,
        "calibration": calibration,
        "accuracy": accuracy,
    }
    
    results_file = DATA_DIR / "calibration_results.json"
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to {results_file}")
    
    return results
