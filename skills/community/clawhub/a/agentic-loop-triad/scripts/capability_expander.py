#!/usr/bin/env python3
"""
Unified Orchestrator v2 — Capability Expander
Paradigm Shift 3: Autonomous Re-specification

When the system detects that a specification is no longer achievable given
observed constraints, it generates a revised specification with adjusted
criteria, documents the revision rationale, and allows the pipeline to
continue — without human intervention.

Usage:
  python capability_expander.py expand --spec specification.json --history cycles_history.json --output-dir .
  python capability_expander.py check --spec specification.json --history cycles_history.json
"""
import json
import sys
import hashlib
import argparse
from pathlib import Path
from datetime import datetime, timezone
from copy import deepcopy
from typing import Optional


def log(msg: str, level: str = "INFO"):
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    icons = {"OK": "✓", "FAIL": "✗", "WARN": "⚠", "INFO": " ", "STAGE": "▶"}
    print(f"[{ts}] {icons.get(level, ' ')} {msg}")


def _detect_impossible_criteria(spec: dict, history: list, threshold: int = 3) -> list:
    """
    Identify success criteria that have never been met in `threshold` consecutive cycles.
    Returns a list of impossible criteria with their history.
    """
    impossible = []
    success_criteria = spec.get("success_criteria", {})

    for criterion, target in success_criteria.items():
        if not isinstance(target, (int, float)):
            continue

        # Determine direction: lower-is-better criteria use "_ms", "_time", "_latency", "_cost", "_error"
        lower_is_better_keywords = ("_ms", "_time", "_latency", "_cost", "_error", "_failures", "_loss")
        lower_is_better = any(criterion.lower().endswith(k) or k in criterion.lower() for k in lower_is_better_keywords)
        # Look at this criterion across all cycles in history
        failures = []
        for cycle_data in history:
            actual = cycle_data.get("metrics", {}).get(criterion)
            if actual is None:
                continue
            # For lower-is-better: met if actual <= target; for higher-is-better: met if actual >= target
            if lower_is_better:
                met = actual <= target
            else:
                met = actual >= target if target >= 0 else actual <= abs(target)
            failures.append({
                "cycle": cycle_data.get("cycle", "?"),
                "target": target,
                "actual": actual,
                "met": met
            })

        if len(failures) >= threshold:
            recent = failures[-threshold:]
            if not any(f["met"] for f in recent):
                # Never met in the last `threshold` cycles
                actuals = [f["actual"] for f in recent if f["actual"] is not None]
                best_actual = max(actuals) if actuals else None
                impossible.append({
                    "criterion": criterion,
                    "target": target,
                    "best_actual": best_actual,
                    "consecutive_failures": len(recent),
                    "history": recent
                })

    return impossible


def _compute_revised_target(criterion: str, target: float, best_actual: Optional[float], history: list) -> dict:
    """
    Compute a revised target for an impossible criterion.
    Strategy: use the best observed actual value with a 10% buffer, or
    reduce the target by 20% if no actuals are available.
    """
    if best_actual is not None and best_actual > 0:
        # Set revised target to best_actual * 0.95 (5% below best observed)
        # This is achievable but still challenging
        revised = round(best_actual * 0.95, 4)
        rationale = f"Original target {target} never achieved in {len(history)} cycles. Best observed: {best_actual}. Revised to {revised} (5% below best observed)."
    else:
        # Reduce by 20%
        revised = round(target * 0.80, 4)
        rationale = f"Original target {target} never achieved and no actuals available. Revised to {revised} (20% reduction)."

    return {
        "original": target,
        "revised": revised,
        "rationale": rationale,
        "revision_type": "best_observed_buffer" if best_actual else "percentage_reduction"
    }



def generate_revised_specification(spec: dict, history: list, threshold: int = 3) -> dict:
    """
    Generate a revised specification with adjusted success criteria for
    any criterion that has been impossible to meet.

    Returns:
        {
            "needs_revision": bool,
            "revised_specification": dict or None,
            "revision_rationale": dict,
            "impossible_criteria": list
        }
    """
    impossible = _detect_impossible_criteria(spec, history, threshold)

    if not impossible:
        return {
            "needs_revision": False,
            "revised_specification": None,
            "revision_rationale": {
                "summary": "No impossible criteria detected. Specification remains unchanged.",
                "impossible_criteria": []
            },
            "impossible_criteria": []
        }

    # Build revised specification
    revised_spec = deepcopy(spec)
    revisions = []

    for item in impossible:
        criterion = item["criterion"]
        target = item["target"]
        best_actual = item.get("best_actual")

        revision = _compute_revised_target(criterion, target, best_actual, item["history"])
        revised_spec["success_criteria"][criterion] = revision["revised"]
        revisions.append({
            "criterion": criterion,
            **revision
        })

    # Update spec metadata
    original_id = spec.get("specification_id", "unknown")
    revised_spec["specification_id"] = f"{original_id}-revised-{hashlib.sha256(str(revisions).encode()).hexdigest()[:8]}"
    revised_spec["version"] = f"{spec.get('version', '1.0')}-auto-revised"
    revised_spec["auto_revised"] = True
    revised_spec["revision_timestamp"] = datetime.now(timezone.utc).isoformat()
    revised_spec["original_specification_id"] = original_id

    # Build human-readable rationale
    rationale = {
        "summary": f"{len(impossible)} criterion/criteria were impossible to meet after {threshold} consecutive cycles. Specification auto-revised.",
        "original_specification_id": original_id,
        "revised_specification_id": revised_spec["specification_id"],
        "revised_at": revised_spec["revision_timestamp"],
        "revisions": revisions,
        "impossible_criteria": impossible,
        "recommendation": "Review the revised targets to ensure they still represent meaningful progress toward the original goal. If the original targets are non-negotiable, investigate the execution environment for systemic constraints."
    }

    return {
        "needs_revision": True,
        "revised_specification": revised_spec,
        "revision_rationale": rationale,
        "impossible_criteria": impossible
    }


def format_revision_rationale_md(rationale: dict) -> str:
    """Format the revision rationale as a human-readable Markdown document."""
    lines = [
        "# Auto-Revision Rationale",
        "",
        f"**Generated:** {rationale.get('revised_at', 'unknown')}",
        f"**Original Specification:** `{rationale.get('original_specification_id', 'unknown')}`",
        f"**Revised Specification:** `{rationale.get('revised_specification_id', 'unknown')}`",
        "",
        "## Summary",
        "",
        rationale.get("summary", ""),
        "",
        "## Revised Criteria",
        "",
        "| Criterion | Original Target | Revised Target | Rationale |",
        "| :--- | :--- | :--- | :--- |"
    ]

    for r in rationale.get("revisions", []):
        lines.append(f"| `{r['criterion']}` | `{r['original']}` | `{r['revised']}` | {r['rationale']} |")

    lines += [
        "",
        "## Recommendation",
        "",
        rationale.get("recommendation", ""),
        "",
        "## Failure History",
        ""
    ]

    for item in rationale.get("impossible_criteria", []):
        lines.append(f"### `{item['criterion']}`")
        lines.append(f"- Target: `{item['target']}`")
        lines.append(f"- Best Observed: `{item.get('best_actual', 'N/A')}`")
        lines.append(f"- Consecutive Failures: `{item['consecutive_failures']}`")
        lines.append("")

    return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Unified Orchestrator Capability Expander")
    subparsers = parser.add_subparsers(dest="command")

    check_parser = subparsers.add_parser("check", help="Check if re-specification is needed")
    check_parser.add_argument("--spec", required=True)
    check_parser.add_argument("--history", required=True, help="Path to cycles_history.json")
    check_parser.add_argument("--threshold", type=int, default=3)

    expand_parser = subparsers.add_parser("expand", help="Generate revised specification")
    expand_parser.add_argument("--spec", required=True)
    expand_parser.add_argument("--history", required=True)
    expand_parser.add_argument("--threshold", type=int, default=3)
    expand_parser.add_argument("--output-dir", default=".")

    args = parser.parse_args()

    if args.command in ("check", "expand"):
        spec = json.loads(Path(args.spec).read_text())
        history = json.loads(Path(args.history).read_text()) if Path(args.history).exists() else []
        result = generate_revised_specification(spec, history, threshold=args.threshold)

        if args.command == "check":
            if result["needs_revision"]:
                log(f"Re-specification needed: {len(result['impossible_criteria'])} impossible criterion/criteria detected.", "WARN")
                for item in result["impossible_criteria"]:
                    log(f"  {item['criterion']}: target={item['target']}, best_actual={item.get('best_actual', 'N/A')}, failures={item['consecutive_failures']}", "WARN")
            else:
                log("No re-specification needed. All criteria are achievable.", "OK")

        elif args.command == "expand":
            out = Path(args.output_dir)
            out.mkdir(parents=True, exist_ok=True)

            if result["needs_revision"]:
                revised_path = out / "revised_specification.json"
                revised_path.write_text(json.dumps(result["revised_specification"], indent=2))
                log(f"Revised specification saved: {revised_path}", "OK")

                rationale_md = format_revision_rationale_md(result["revision_rationale"])
                rationale_path = out / "revision_rationale.md"
                rationale_path.write_text(rationale_md)
                log(f"Revision rationale saved: {rationale_path}", "OK")

                rationale_json_path = out / "revision_rationale.json"
                rationale_json_path.write_text(json.dumps(result["revision_rationale"], indent=2))
            else:
                log("No revision needed. No files written.", "OK")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
