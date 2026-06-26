#!/usr/bin/env python3
"""
Iteration engine: measure -> rewrite -> re-measure loop.

Produces targeted feedback for the orchestrating LLM to perform rewrites.
All rewriting is done locally by the LLM — no external API calls.

Usage:
  python iterate.py --file essay.txt [--max-iters 3] [--threshold 15]
  python iterate.py --text "..." --json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from measure import (
    measure,
    AI_SCORE_THRESHOLD,
    MDD_MEAN_LOW,
    MDD_MEAN_HIGH,
    MDD_VARIANCE_MIN,
    TTR_MIN,
    CONTENT_WORD_RATIO_LOW,
    CONTENT_WORD_RATIO_HIGH,
    HUMAN_MDD_MEAN,
    HUMAN_MDD_VARIANCE,
)


def build_iteration_feedback(report: Dict[str, Any], iteration: int) -> str:
    """Convert a measurement report into targeted natural-language revision instructions."""
    lines: List[str] = []
    lines.append(f"=== Iteration {iteration} Revision Instructions ===")

    if not report["ai_pattern_pass"]:
        flagged = sorted(
            [p for p in report["pattern_details"] if p["count"] > 0 and p["weight"] > 0],
            key=lambda p: p["contribution"],
            reverse=True,
        )

        if iteration == 1:
            targets = flagged[:4]
            lines.append("PRIORITY: Remove the highest-weight AI writing patterns:")
        elif iteration == 2:
            targets = flagged
            lines.append("Fix ALL remaining AI writing patterns:")
        else:
            targets = flagged
            lines.append("Fine-tune: eliminate last AI pattern traces:")

        for p in targets:
            lines.append(
                f"  - {p['name']}: found {p['count']} instances "
                f"({p['density_per_1k']}/1k words). Remove or rephrase."
            )

    syn = report["syntactic"]
    if not syn.get("mdd_pass", True):
        if syn["mdd_variance"] < MDD_VARIANCE_MIN:
            lines.append(
                f"SYNTACTIC: MDD variance is {syn['mdd_variance']:.4f} "
                f"(target >= {MDD_VARIANCE_MIN}). Vary sentence structure more: "
                f"mix short declarative sentences with longer complex ones."
            )
        if syn["mdd_mean"] < MDD_MEAN_LOW:
            lines.append(
                f"SYNTACTIC: MDD mean {syn['mdd_mean']:.4f} is too low "
                f"(target {MDD_MEAN_LOW}-{MDD_MEAN_HIGH}). "
                f"Add some longer-distance dependencies."
            )
        elif syn["mdd_mean"] > MDD_MEAN_HIGH:
            lines.append(
                f"SYNTACTIC: MDD mean {syn['mdd_mean']:.4f} is too high. "
                f"Break some complex sentences into simpler ones."
            )

    sem = report["semantic"]
    if not sem.get("ttr_pass", True):
        lines.append(
            f"SEMANTIC: TTR is {sem['ttr']:.4f} (target >= {TTR_MIN}). "
            f"Use more varied vocabulary; avoid repeating the same content words."
        )
    if not sem.get("ratio_pass", True):
        cwr = sem["content_word_ratio"]
        if cwr < CONTENT_WORD_RATIO_LOW:
            lines.append(
                f"SEMANTIC: Content-word ratio {cwr:.4f} too low. "
                f"Reduce function words; make prose more information-dense."
            )
        elif cwr > CONTENT_WORD_RATIO_HIGH:
            lines.append(
                f"SEMANTIC: Content-word ratio {cwr:.4f} too high. "
                f"Add natural connectives and transitions."
            )

    lines.append("")
    lines.append("CONSTRAINTS: Preserve the author's argument, citations, and structure. "
                  "Do not invent new sources. Output plain text only.")
    return "\n".join(lines)


def iterate_humanize(
    essay: str,
    max_iters: int = 3,
    ai_threshold: float = AI_SCORE_THRESHOLD,
) -> Dict[str, Any]:
    """
    Measure the essay and produce targeted feedback for the LLM to rewrite.

    This function handles measurement only. The orchestrating LLM performs
    the actual rewriting based on the feedback — no external API calls.

    Returns:
        {
            "final_essay": str,
            "iterations": [report, ...],
            "converged": bool,
            "total_iterations": int,
            "pending_feedback": str (if not converged),
        }
    """
    current = essay
    history: List[Dict[str, Any]] = []

    for i in range(1, max_iters + 1):
        report = measure(current)
        report["iteration"] = i
        history.append(report)

        if report["passes"]:
            return {
                "final_essay": current,
                "iterations": history,
                "converged": True,
                "total_iterations": i,
            }

        feedback = build_iteration_feedback(report, i)

        print(f"\n[ITERATION {i}] Rewrite needed.", file=sys.stderr)
        print(f"[FEEDBACK]\n{feedback}", file=sys.stderr)
        return {
            "final_essay": current,
            "iterations": history,
            "converged": False,
            "total_iterations": i,
            "pending_feedback": feedback,
        }

    # Ran out of iterations
    final_report = measure(current)
    final_report["iteration"] = max_iters + 1
    history.append(final_report)

    return {
        "final_essay": current,
        "iterations": history,
        "converged": final_report["passes"],
        "total_iterations": max_iters,
    }


def format_iteration_table(result: Dict[str, Any]) -> str:
    """Format iteration history as a markdown table."""
    lines = [
        "| Iter | AI Score | MDD Mean | MDD Var  | TTR    | CW Ratio | Status |",
        "|------|----------|----------|----------|--------|----------|--------|",
    ]
    for report in result["iterations"]:
        it = report.get("iteration", "?")
        ai = report["ai_pattern_score"]
        mdd_m = report["syntactic"]["mdd_mean"]
        mdd_v = report["syntactic"]["mdd_variance"]
        ttr = report["semantic"]["ttr"]
        cwr = report["semantic"]["content_word_ratio"]
        status = "PASS" if report["passes"] else "FAIL"
        lines.append(
            f"| {it:>4} | {ai:>8.1f} | {mdd_m:>8.4f} | {mdd_v:>8.4f} | {ttr:>6.4f} | {cwr:>8.4f} | {status:>6} |"
        )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Iteratively humanize an essay")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", type=str, help="Essay text (inline)")
    group.add_argument("--file", type=str, help="Path to essay text file")
    parser.add_argument("--max-iters", type=int, default=3)
    parser.add_argument("--threshold", type=float, default=AI_SCORE_THRESHOLD)
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    else:
        text = args.text

    result = iterate_humanize(
        essay=text,
        max_iters=args.max_iters,
        ai_threshold=args.threshold,
    )

    if args.json:
        output = {k: v for k, v in result.items() if k != "final_essay"}
        output["final_essay_length"] = len(result["final_essay"])
        print(json.dumps(output, indent=2, ensure_ascii=False))
        print("\n--- FINAL ESSAY ---")
        print(result["final_essay"])
    else:
        print(f"\n{'='*60}")
        print(f"  Iteration Result: {'CONVERGED' if result['converged'] else 'DID NOT CONVERGE'}")
        print(f"  Iterations used: {result['total_iterations']}")
        print(f"{'='*60}\n")
        print(format_iteration_table(result))
        if result.get("pending_feedback"):
            print(f"\n--- Pending Feedback (API fallback) ---")
            print(result["pending_feedback"])
        print(f"\n--- FINAL ESSAY ({len(result['final_essay'])} chars) ---")
        print(result["final_essay"])


if __name__ == "__main__":
    main()
