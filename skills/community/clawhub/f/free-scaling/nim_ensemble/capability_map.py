#!/usr/bin/env python3
"""Model capability cartography — multi-trial profiling with error correlation analysis.

Runs each test N times per model to estimate:
- Per-category accuracy + variance (stability)
- Pairwise error correlation (complementarity)
- Recommended panels based on actual capability data

Output: capability_map.json with per-model profiles + correlation matrix + routing policy.
"""

import json
import os
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nim_ensemble import call_model, MODELS, parse_answer
from nim_ensemble.benchmark import CAPABILITY_TESTS


@dataclass
class TrialResult:
    model: str
    category: str
    test_idx: int
    trial: int
    answer: str
    correct: bool
    latency: float
    raw: str = ""


def run_single_trial(model: str, test_idx: int, cat: str, prompt: str, 
                     truth: str, acceptable: list, trial: int) -> TrialResult:
    """Run one trial of one test on one model."""
    t0 = time.time()
    ans, raw = call_model(prompt, model)
    dt = time.time() - t0
    
    # Re-parse with acceptable patterns if default parse missed
    if ans not in acceptable and ans != "ERROR":
        ans2 = parse_answer(raw, patterns=acceptable + ["UNCLEAR"])
        if ans2 in acceptable:
            ans = ans2
    
    # Numeric answer check
    if ans not in acceptable and truth.isdigit():
        first_line = raw.strip().split("\n")[0].strip()
        if truth in first_line:
            ans = truth
    
    correct = ans in acceptable
    # UNCLEAR is correct for calibration
    if ans == "UNCLEAR" and "UNCLEAR" in acceptable:
        correct = True
    
    return TrialResult(
        model=model, category=cat, test_idx=test_idx,
        trial=trial, answer=ans, correct=correct,
        latency=dt, raw=raw[:200],
    )


def run_model_profile(model: str, n_trials: int = 3, 
                      max_parallel: int = 5) -> list[TrialResult]:
    """Profile one model across all tests with N trials each. Parallelized within model."""
    all_trials = []
    tasks = []
    
    for idx, (cat, prompt, truth, acceptable) in enumerate(CAPABILITY_TESTS):
        for trial in range(n_trials):
            tasks.append((model, idx, cat, prompt, truth, acceptable, trial))
    
    # Throttle to avoid NIM rate limits (40 RPM shared)
    # Run in batches of max_parallel
    for batch_start in range(0, len(tasks), max_parallel):
        batch = tasks[batch_start:batch_start + max_parallel]
        with ThreadPoolExecutor(max_workers=len(batch)) as pool:
            futures = [pool.submit(run_single_trial, *t) for t in batch]
            for fut in as_completed(futures):
                try:
                    all_trials.append(fut.result())
                except Exception as e:
                    print(f"  Error: {e}", file=sys.stderr)
        
        # Small delay between batches to respect rate limits
        if batch_start + max_parallel < len(tasks):
            time.sleep(0.5)
    
    return all_trials


def compute_model_profile(trials: list[TrialResult]) -> dict:
    """Compute capability profile from trial results."""
    by_cat = defaultdict(lambda: {"correct": 0, "total": 0, "latencies": []})
    by_test = defaultdict(list)  # test_idx -> [correct bools]
    
    for t in trials:
        by_cat[t.category]["total"] += 1
        if t.correct:
            by_cat[t.category]["correct"] += 1
        by_cat[t.category]["latencies"].append(t.latency)
        by_test[t.test_idx].append(t.correct)
    
    total_correct = sum(v["correct"] for v in by_cat.values())
    total_tests = sum(v["total"] for v in by_cat.values())
    all_latencies = [t.latency for t in trials]
    
    category_scores = {}
    for cat, stats in sorted(by_cat.items()):
        acc = stats["correct"] / stats["total"] if stats["total"] else 0
        avg_lat = sum(stats["latencies"]) / len(stats["latencies"]) if stats["latencies"] else 0
        category_scores[cat] = {
            "accuracy": round(acc, 3),
            "avg_latency_s": round(avg_lat, 2),
            "n_trials": stats["total"],
        }
    
    # Per-test stability (how often does it get the same answer?)
    stability_scores = []
    for idx, correctness_list in by_test.items():
        # Stability = fraction of trials that agree with majority
        c = Counter(correctness_list)
        majority = c.most_common(1)[0][1]
        stability_scores.append(majority / len(correctness_list))
    
    avg_stability = sum(stability_scores) / len(stability_scores) if stability_scores else 0
    
    # Identify strengths/weaknesses
    strengths = [cat for cat, s in category_scores.items() if s["accuracy"] >= 0.9]
    weaknesses = [cat for cat, s in category_scores.items() if s["accuracy"] < 0.6]
    
    return {
        "accuracy": round(total_correct / total_tests, 3) if total_tests else 0,
        "avg_latency_s": round(sum(all_latencies) / len(all_latencies), 2) if all_latencies else 0,
        "stability": round(avg_stability, 3),
        "category_scores": category_scores,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "n_trials_per_test": len(by_test[0]) if 0 in by_test else 0,
    }


def compute_error_correlation(all_model_trials: dict[str, list[TrialResult]]) -> dict:
    """Compute pairwise error correlation between models.
    
    For each pair (A, B), compute:
    - agreement_rate: how often they give the same correctness
    - error_correlation: Pearson correlation of error patterns
    - complementarity: 1 - error_correlation (higher = more diverse)
    
    Low correlation = good ensemble partners.
    """
    models = sorted(all_model_trials.keys())
    
    # Build per-test correctness vectors (majority across trials)
    test_correctness = {}
    for model, trials in all_model_trials.items():
        by_test = defaultdict(list)
        for t in trials:
            by_test[t.test_idx].append(t.correct)
        
        # Majority vote per test
        test_correctness[model] = {}
        for idx, bools in by_test.items():
            test_correctness[model][idx] = sum(bools) > len(bools) / 2
    
    # Common test indices
    all_indices = set()
    for tc in test_correctness.values():
        all_indices.update(tc.keys())
    common = sorted(all_indices)
    
    correlations = {}
    for i, m1 in enumerate(models):
        for m2 in models[i+1:]:
            v1 = [int(test_correctness[m1].get(idx, False)) for idx in common]
            v2 = [int(test_correctness[m2].get(idx, False)) for idx in common]
            
            # Agreement rate
            agree = sum(a == b for a, b in zip(v1, v2)) / len(common) if common else 0
            
            # Error pattern: 1 = error, 0 = correct
            e1 = [1 - x for x in v1]
            e2 = [1 - x for x in v2]
            
            # Pearson correlation of errors
            n = len(common)
            if n < 2:
                corr = 0
            else:
                mean1 = sum(e1) / n
                mean2 = sum(e2) / n
                cov = sum((a - mean1) * (b - mean2) for a, b in zip(e1, e2)) / n
                std1 = (sum((a - mean1)**2 for a in e1) / n) ** 0.5
                std2 = (sum((b - mean2)**2 for b in e2) / n) ** 0.5
                if std1 * std2 == 0:
                    corr = 0  # one or both models have zero errors
                else:
                    corr = cov / (std1 * std2)
            
            pair_key = f"{m1}+{m2}"
            correlations[pair_key] = {
                "agreement": round(agree, 3),
                "error_correlation": round(corr, 3),
                "complementarity": round(1 - abs(corr), 3),
            }
    
    return correlations


def generate_routing_policy(profiles: dict, correlations: dict) -> dict:
    """Generate optimal panel recommendations based on capability data."""
    
    policy = {
        "recommended_panels": {},
        "per_category_weights": {},
        "escalation_rules": [],
    }
    
    # Find best models per category
    for cat in ["instruction", "factual", "nuance", "reasoning", "code", 
                "calibration", "agreeableness"]:
        ranked = []
        for model, prof in profiles.items():
            cs = prof["category_scores"].get(cat, {})
            if cs.get("n_trials", 0) > 0:
                ranked.append((model, cs["accuracy"], cs["avg_latency_s"]))
        
        ranked.sort(key=lambda x: (-x[1], x[2]))  # accuracy desc, latency asc
        policy["per_category_weights"][cat] = {
            "top_models": [(m, acc) for m, acc, _ in ranked[:5]],
            "avoid": [m for m, acc, _ in ranked if acc < 0.6],
        }
    
    # Find most complementary pairs/trios
    if correlations:
        pairs = sorted(correlations.items(), key=lambda x: x[1]["complementarity"], reverse=True)
        top_pairs = pairs[:5]
        policy["best_complementary_pairs"] = [
            {"pair": k, **v} for k, v in top_pairs
        ]
    
    # Build recommended panels from data
    all_models = sorted(profiles.keys())
    
    # "accurate" panel: top 3 by overall accuracy
    by_acc = sorted(all_models, key=lambda m: -profiles[m]["accuracy"])
    policy["recommended_panels"]["accurate"] = by_acc[:3]
    
    # "fast_accurate" panel: top 3 by accuracy among fast models
    fast_accurate = sorted(
        [m for m in all_models if profiles[m]["avg_latency_s"] <= 1.5],
        key=lambda m: -profiles[m]["accuracy"]
    )
    policy["recommended_panels"]["fast_accurate"] = fast_accurate[:3]
    
    # "stable" panel: top 3 by stability
    by_stab = sorted(all_models, key=lambda m: -profiles[m].get("stability", 0))
    policy["recommended_panels"]["stable"] = by_stab[:3]
    
    # "nuance" panel: best at nuance + agreeableness
    nuance_score = lambda m: (
        profiles[m]["category_scores"].get("nuance", {}).get("accuracy", 0) +
        profiles[m]["category_scores"].get("agreeableness", {}).get("accuracy", 0)
    ) / 2
    by_nuance = sorted(all_models, key=lambda m: -nuance_score(m))
    policy["recommended_panels"]["nuance"] = by_nuance[:3]
    
    # "reasoning" panel: best at reasoning + factual
    reason_score = lambda m: (
        profiles[m]["category_scores"].get("reasoning", {}).get("accuracy", 0) +
        profiles[m]["category_scores"].get("factual", {}).get("accuracy", 0)
    ) / 2
    by_reason = sorted(all_models, key=lambda m: -reason_score(m))
    policy["recommended_panels"]["reasoning"] = by_reason[:3]
    
    # Escalation rules
    policy["escalation_rules"] = [
        "If fast panel is unanimous → accept (high confidence)",
        "If fast panel splits → escalate to deep panel",
        "If deep panel also splits → escalate to max panel (5 models)",
        "If max panel <60% agreement → flag UNCERTAIN for human review",
        "For nuance/agreeableness tasks → use nuance panel directly",
        "For reasoning/factual tasks → use reasoning panel directly",
    ]
    
    return policy


def run_capability_map(
    models: list[str] = None,
    n_trials: int = 3,
    max_parallel_per_model: int = 4,
    output_path: str = "capability_map.json",
    verbose: bool = True,
):
    """Run full capability cartography."""
    if models is None:
        models = list(MODELS.keys())
    
    n_tests = len(CAPABILITY_TESTS)
    total_calls = len(models) * n_tests * n_trials
    print(f"Capability Map: {len(models)} models × {n_tests} tests × {n_trials} trials = {total_calls} API calls")
    print(f"Estimated time: {total_calls * 1.5 / max_parallel_per_model :.0f}s")
    print()
    
    all_model_trials = {}
    profiles = {}
    
    # Run models (serialize to avoid rate limits, but parallelize within)
    for i, model in enumerate(sorted(models)):
        t0 = time.time()
        if verbose:
            print(f"[{i+1}/{len(models)}] Profiling {model}...", end=" ", flush=True)
        
        trials = run_model_profile(model, n_trials, max_parallel_per_model)
        all_model_trials[model] = trials
        profiles[model] = compute_model_profile(trials)
        
        dt = time.time() - t0
        p = profiles[model]
        if verbose:
            print(f"{p['accuracy']:.0%} accuracy, {p['stability']:.0%} stability, {p['avg_latency_s']:.1f}s avg ({dt:.0f}s total)")
            if p["weaknesses"]:
                print(f"    ⚠️  Weak: {', '.join(p['weaknesses'])}")
    
    # Compute error correlations
    print(f"\nComputing error correlations...")
    correlations = compute_error_correlation(all_model_trials)
    
    # Generate routing policy
    print("Generating routing policy...")
    policy = generate_routing_policy(profiles, correlations)
    
    # Assemble output
    capability_map = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "n_trials": n_trials,
        "n_tests": n_tests,
        "n_models": len(models),
        "total_api_calls": total_calls,
        "profiles": profiles,
        "error_correlations": correlations,
        "routing_policy": policy,
    }
    
    with open(output_path, "w") as f:
        json.dump(capability_map, f, indent=2)
    print(f"\nCapability map saved to {output_path}")
    
    # Print summary
    print(f"\n{'='*70}")
    print(f"{'Model':<22} {'Acc':>5} {'Stab':>5} {'Lat':>5}  {'Strengths':<30} {'Weak'}")
    print("-" * 90)
    for model in sorted(profiles, key=lambda m: -profiles[m]["accuracy"]):
        p = profiles[model]
        strengths = ", ".join(p["strengths"][:3]) or "-"
        weak = ", ".join(p["weaknesses"]) or "-"
        print(f"{model:<22} {p['accuracy']:>4.0%} {p['stability']:>4.0%} {p['avg_latency_s']:>4.1f}s  {strengths:<30} {weak}")
    
    if correlations:
        print(f"\nMost complementary pairs:")
        sorted_pairs = sorted(correlations.items(), key=lambda x: x[1]["complementarity"], reverse=True)
        for pair, stats in sorted_pairs[:5]:
            print(f"  {pair:<35} complementarity={stats['complementarity']:.2f}  agreement={stats['agreement']:.0%}")
    
    print(f"\nRecommended panels:")
    for name, models_list in policy["recommended_panels"].items():
        print(f"  {name:<20} {', '.join(models_list)}")
    
    return capability_map


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="NIM model capability cartography")
    parser.add_argument("--models", "-m", nargs="*", help="Model aliases (default: all)")
    parser.add_argument("--trials", "-n", type=int, default=3, help="Trials per test (default 3)")
    parser.add_argument("--parallel", "-p", type=int, default=4, help="Parallel calls per model")
    parser.add_argument("--speed", "-s", help="Filter models by speed tier")
    parser.add_argument("--output", "-o", default="capability_map.json")
    parser.add_argument("--quiet", "-q", action="store_true")
    args = parser.parse_args()
    
    models = args.models
    if not models and args.speed:
        from nim_ensemble import list_models
        models = list_models(speed=args.speed)
    
    run_capability_map(
        models=models,
        n_trials=args.trials,
        max_parallel_per_model=args.parallel,
        output_path=args.output,
        verbose=not args.quiet,
    )
