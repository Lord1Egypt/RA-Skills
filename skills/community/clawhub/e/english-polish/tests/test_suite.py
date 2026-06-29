#!/usr/bin/env python3
"""
english-polish Phase 0 Detector — Test Suite
=============================================
Run: python3 test_suite.py

Tests:
  1. Set A: 18 known Chinglish sentences (one per pattern A-S)
  2. Set B: 5 clean native-English paragraphs
  3. Set C: 5 boundary cases (literary English, quotes, technical writing)
  4. Full book baseline (optional, requires --full)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from detector import analyze_text, PATTERNS

# ── Test Sets ────────────────────────────────────────────────────────

SET_A = {
    "A_subject_dangling": "For chip design, competition is fierce among all players.",
    "B_as_for_redundant": "As for the energy cost, it is becoming the main constraint.",
    "C_passive_chain": "It can be seen that the market is being reshaped by export controls.",
    "D_make_abstract_noun": "We need to make a comparison between the two approaches.",
    "E_not_only_but_also": "Not only did NVIDIA dominate hardware, but also it built a software ecosystem.",
    "F_noun_stacking": "Data center GPU market growth prediction models are inaccurate.",
    "G_should_false": "China should develop its own chip industry to reduce dependency.",
    "H_the_overuse": "The computing power is the most important resource.",
    "I_chinese_filler": "To a certain extent, competition benefits consumers.",
    "J_this_is_because": "This is because the technological barriers are high.",
    "K_redundant_modifier": "Companies should actively strengthen their supply chain resilience.",
    "L_weak_verb_nominalization": "The team conducted research on GPU design.",
    "M_emphasis_inversion": "It is this gap that explains the performance difference.",
    "N_list_cadence": "First, the market is growing. Second, competition is intensifying.",
    "O_concessive_cluster": "Although the market is large, but competition is fierce.",
    "P_topic_comment": "As for NVIDIA, it dominates the AI market.",
    "Q_false_inclusive": "We can see that the landscape is changing rapidly.",
    "R_logical_sawtooth": "On one hand, the market is growing. On the other hand, competition is intense.",
    "S_list_summarizer": "All these factors contribute to the market growth.",
}

# Clean native English — should score 4.5+
SET_B = [
    "NVIDIA dominates the AI chip market because it built a decade-long software ecosystem around CUDA. No competitor has replicated this moat.",
    "AMD's MI300X delivers competitive raw performance, but its software stack lags behind CUDA's maturity.",
    "The semiconductor industry faces two structural constraints: rising design costs and slowing lithographic returns.",
    "Data center power consumption doubled between 2019 and 2024, driven primarily by AI training workloads.",
    "Capital expenditure on cloud infrastructure surpassed $150 billion in 2025, with hyperscalers accounting for 70% of spending.",
]

# Boundary cases — literary/classic English that should NOT trigger patterns
SET_C = [
    # Literary: classic English from Shakespeare
    "To be, or not to be, that is the question: Whether 'tis nobler in the mind to suffer the slings and arrows of outrageous fortune.",
    # Technical: dense academic writing
    "The relationship between supply voltage and switching frequency follows a power-law distribution under subthreshold operating conditions.",
    # Quoted speech: casual native English
    '"We should probably just ship it and fix the bugs later," the engineer said.',
    # Complex native English with embedding
    "What matters is not the quantity of compute but its utilization rate—a metric that most data centers track only loosely.",
    # Perfect native sentence (should be clean)
    "Tightening monetary conditions force a reassessment of growth assumptions, particularly for high-duration assets.",
]

# ── Test Runner ──────────────────────────────────────────────────────

PASS = "✅"
FAIL = "❌"
PARTIAL = "⚠️"

results = {"passed": 0, "failed": 0, "partial": 0, "details": []}


def test_pattern(key: str, text: str):
    """Test that a specific known Chinglish sentence triggers its pattern."""
    result = analyze_text(text)
    categories = result.get("categories_detected", {})

    # Match: check if any detected category key starts with our test prefix
    # This handles short test keys like "M_emphasis_inversion" vs full key "M_chinese_emphasis_inversion"
    prefix = key.split("_")[0]  # e.g., "M" from "M_emphasis_inversion"
    detected = any(k.startswith(prefix) for k in categories)

    score = result["nativization_score"]
    any_detected = len(categories) > 0

    if detected:
        status = PASS
    elif any_detected:
        status = PARTIAL  # something detected but not our pattern
    else:
        status = FAIL  # nothing detected

    cat_names = list(categories.keys())
    detail = f"  {status} [{key:25s}] score={score:.1f}  detected={detected}, total={len(cat_names)}"
    if status != PASS or cat_names:
        detail += f"  triggered={cat_names}"

    return status, score, detail


def test_clean(text: str, expected_min: float = 4.0):
    """Test that clean native English scores above threshold."""
    result = analyze_text(text)
    score = result["nativization_score"]
    score_ok = score >= expected_min
    status = PASS if score_ok else FAIL

    detail = f"  {status} score={score:.1f}  (threshold≥{expected_min})  issues={result['total_weighted_issues']}"
    if not score_ok:
        detail += f"  detected={list(result.get('categories_detected', {}).keys())[:3]}"

    return status, score, detail


def run_all():
    print("=" * 70)
    print("english-polish Phase 0 Detector — Test Suite v2 (19 patterns)")
    print("=" * 70)

    # ── Set A: Known Chinglish ──
    print(f"\n{'─'*70}")
    print(f"📋 Set A: 19 known Chinglish sentences (one per pattern A-S)")
    print(f"{'─'*70}")
    for key, text in SET_A.items():
        status, score, detail = test_pattern(key, text)
        # Show expected pattern label
        label = PATTERNS.get(key, {}).get("label", key)
        print(f"  [{label}]\n{detail}")
        if status == PASS:
            results["passed"] += 1
        elif status == FAIL:
            results["failed"] += 1
        else:
            results["partial"] += 1
        results["details"].append({"set": "A", "key": key, "status": status, "score": score})

    # ── Set B: Clean English ──
    print(f"\n{'─'*70}")
    print(f"📋 Set B: 5 clean native-English paragraphs")
    print(f"{'─'*70}")
    for i, text in enumerate(SET_B):
        status, score, detail = test_clean(text, expected_min=4.0)
        print(f"  Sample B{i+1}:\n{detail}")
        if status == PASS:
            results["passed"] += 1
        else:
            results["failed"] += 1
        results["details"].append({"set": "B", "sample": i, "status": status, "score": score})

    # ── Set C: Boundary Cases ──
    print(f"\n{'─'*70}")
    print(f"📋 Set C: 5 boundary cases (literary/technical/casual)")
    print(f"{'─'*70}")
    for i, text in enumerate(SET_C):
        # Literary/classic English should score >= 4.0
        threshold = 3.5 if i == 2 else 4.0  # quoted speech might score slightly lower
        status, score, detail = test_clean(text, expected_min=threshold)
        label = ["Literary (Shakespeare)", "Technical dense", "Quoted speech", "Complex native", "Perfect sentence"][i]
        print(f"  {label}:\n{detail}")
        if status == PASS:
            results["passed"] += 1
        else:
            results["failed"] += 1
        results["details"].append({"set": "C", "sample": i, "status": status, "score": score})

    # ── Summary ──
    print(f"\n{'='*70}")
    total = results["passed"] + results["failed"] + results["partial"]
    print(f"RESULTS: {PASS} {results['passed']}/{total} passed  {FAIL} {results['failed']} failed  {PARTIAL} {results['partial']} partial")
    covered = sum(
        1 for d in results["details"] if d["set"] == "A" and d["status"] == PASS
    )
    print(f"  Set A (patterns): {covered}/{len(SET_A)} patterns correctly detected")
    print(f"  Set B (clean    ): {sum(1 for d in results['details'] if d['set']=='B' and d['status']==PASS)}/5 clean texts score ≥4.0")
    print(f"  Set C (boundary ): {sum(1 for d in results['details'] if d['set']=='C' and d['status']==PASS)}/5 boundary cases pass")
    print(f"{'='*70}")

    # ⚠️ Warning for failures
    if results["failed"] > 0 or results["partial"] > 0:
        print(f"\n⚠️  {results['failed']} failures + {results['partial']} partials")
        for d in results["details"]:
            if d["status"] != PASS:
                print(f"  {d['status']} {d['set']}:{d.get('key', d.get('sample', '?'))} score={d.get('score','?')}")


if __name__ == "__main__":
    run_all()
