#!/usr/bin/env python3
"""
Unified Orchestrator v2 — Meta Learner
Paradigm Shift 2: Capability Expansion via Meta-Learning
Paradigm Shift 4: Cross-Goal Skill Transfer

Responsibilities:
  - Accumulate learnings across cycles into learnings_log.json
  - Detect recurring failure patterns and high-performing specification patterns
  - Generate specification_patches.json and rule_patches.json after 3+ cycles
  - Maintain goal_similarity_index.json for cross-goal transfer
  - Bootstrap new specifications from the closest prior goal

Usage:
  python meta_learner.py learn --state pipeline_state.json --output-dir .
  python meta_learner.py transfer --goal "new goal text" --index goal_similarity_index.json
  python meta_learner.py index-update --state pipeline_state.json --index goal_similarity_index.json
"""
import json
import sys
import hashlib
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional


def log(msg: str, level: str = "INFO"):
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    icons = {"OK": "✓", "FAIL": "✗", "WARN": "⚠", "INFO": " ", "STAGE": "▶"}
    print(f"[{ts}] {icons.get(level, ' ')} {msg}")


def _keywords(text: str) -> set:
    """Extract meaningful keywords from text for similarity matching."""
    stopwords = {"a", "an", "the", "and", "or", "but", "in", "on", "at", "to",
                 "for", "of", "with", "by", "from", "is", "are", "was", "be",
                 "that", "this", "it", "as", "all", "any", "each", "per"}
    words = set(text.lower().replace(",", " ").replace(".", " ").split())
    return words - stopwords


def goal_similarity(goal_a: str, goal_b: str) -> float:
    """Compute Jaccard similarity between two goal descriptions."""
    kw_a = _keywords(goal_a)
    kw_b = _keywords(goal_b)
    if not kw_a or not kw_b:
        return 0.0
    intersection = len(kw_a & kw_b)
    union = len(kw_a | kw_b)
    return round(intersection / union, 4) if union > 0 else 0.0


# ── Paradigm Shift 2: Meta-Learning ──────────────────────────────────────────

def extract_learnings(state: dict) -> dict:
    """
    Extract learnings from a completed pipeline cycle.
    Returns a learning entry for the learnings_log.
    """
    spec = state.get("specification", {})
    analysis = state.get("analysis", {})
    outcome = state.get("outcome", {})
    drift = state.get("drift_result", {})
    cycle = state.get("cycle", 1)
    goal = state.get("goal", "")

    # Extract failure patterns
    failure_patterns = []
    suggestions = analysis.get("suggestions", [])
    for s in suggestions:
        if s.get("priority") in ("critical", "high"):
            failure_patterns.append({
                "pattern": s.get("description", ""),
                "category": s.get("category", "unknown"),
                "priority": s.get("priority"),
                "effort": s.get("effort_estimate", "medium")
            })

    # Extract what worked well (high performance, low drift)
    perf_score = analysis.get("performance_score", 0)
    alignment_score = analysis.get("alignment", {}).get("alignment_score", 0)
    drift_score = drift.get("drift_score", 1.0)

    success_patterns = []
    if perf_score >= 0.85:
        success_patterns.append({
            "pattern": "high_performance_spec",
            "description": f"Specification achieved performance score {perf_score:.2f}",
            "spec_id": spec.get("specification_id")
        })
    if alignment_score >= 0.90:
        success_patterns.append({
            "pattern": "high_alignment",
            "description": f"Specification achieved alignment score {alignment_score:.2f}",
            "spec_id": spec.get("specification_id")
        })

    # Extract regression tests generated this cycle
    regression_tests = analysis.get("regression_tests", [])

    learning_id = hashlib.sha256(f"{goal}{cycle}{datetime.now().isoformat()}".encode()).hexdigest()[:12]

    return {
        "learning_id": learning_id,
        "goal": goal,
        "cycle": cycle,
        "performance_score": perf_score,
        "alignment_score": alignment_score,
        "drift_score": drift_score,
        "failure_patterns": failure_patterns,
        "success_patterns": success_patterns,
        "regression_tests_generated": len(regression_tests),
        "regression_tests": regression_tests,
        "auto_revised": state.get("auto_revised", False),
        "transfer_applied": state.get("transfer_applied", False),
        "recorded_at": datetime.now(timezone.utc).isoformat()
    }


def update_learnings_log(log_path: Path, new_learning: dict) -> list:
    """Append a new learning to the learnings log."""
    existing = json.loads(log_path.read_text()) if log_path.exists() else []
    updated = existing + [new_learning]
    log_path.write_text(json.dumps(updated, indent=2))
    return updated


def generate_patches(learnings: list, min_cycles: int = 3) -> dict:
    """
    After min_cycles of data, generate:
    - specification_patches: improvements to how specs are written
    - rule_patches: new suggestion rules for the feedback loop analyzer
    """
    if len(learnings) < min_cycles:
        return {
            "ready": False,
            "reason": f"Need {min_cycles} cycles, have {len(learnings)}",
            "specification_patches": [],
            "rule_patches": []
        }

    # Count recurring failure patterns
    pattern_counts = {}
    for learning in learnings:
        for fp in learning.get("failure_patterns", []):
            key = fp.get("category", "unknown")
            pattern_counts[key] = pattern_counts.get(key, 0) + 1

    # Patterns that recur in >50% of cycles are systemic
    systemic_patterns = {k: v for k, v in pattern_counts.items() if v / len(learnings) > 0.5}

    # Build specification patches
    spec_patches = []
    for pattern, count in systemic_patterns.items():
        spec_patches.append({
            "patch_id": f"SP-{hashlib.sha256(pattern.encode()).hexdigest()[:8]}",
            "target": "specification_template",
            "field": "behavioral_scenarios",
            "action": "add_scenario",
            "rationale": f"Pattern '{pattern}' occurred in {count}/{len(learnings)} cycles",
            "suggested_scenario": {
                "scenario": f"Validate against {pattern} failure mode",
                "input": f"Edge case triggering {pattern}",
                "expected_output": "Graceful handling without failure",
                "priority": "high"
            }
        })

    # Build rule patches for feedback-loop analyzer
    rule_patches = []
    avg_perf = sum(l.get("performance_score", 0) for l in learnings) / len(learnings)
    avg_align = sum(l.get("alignment_score", 0) for l in learnings) / len(learnings)

    if avg_perf < 0.75:
        rule_patches.append({
            "patch_id": f"RP-{hashlib.sha256('low_perf'.encode()).hexdigest()[:8]}",
            "target": "suggestion_rules",
            "action": "add_rule",
            "rule": {
                "id": "meta_low_performance",
                "condition": "performance_score < 0.80",
                "priority": "high",
                "suggestion": "Performance consistently below 0.80 across cycles. Review success criteria calibration.",
                "category": "performance"
            }
        })

    if avg_align < 0.80:
        rule_patches.append({
            "patch_id": f"RP-{hashlib.sha256('low_align'.encode()).hexdigest()[:8]}",
            "target": "suggestion_rules",
            "action": "add_rule",
            "rule": {
                "id": "meta_low_alignment",
                "condition": "alignment_score < 0.80",
                "priority": "high",
                "suggestion": "Alignment consistently below 0.80. Review shared_intent values against goal definition.",
                "category": "alignment"
            }
        })

    # Find best-performing specification for transfer
    best_learning = max(learnings, key=lambda l: l.get("performance_score", 0) + l.get("alignment_score", 0))

    return {
        "ready": True,
        "cycles_analyzed": len(learnings),
        "systemic_patterns": systemic_patterns,
        "specification_patches": spec_patches,
        "rule_patches": rule_patches,
        "best_performing_cycle": best_learning.get("cycle"),
        "best_performing_spec_id": best_learning.get("learning_id"),
        "average_performance": round(avg_perf, 4),
        "average_alignment": round(avg_align, 4),
        "generated_at": datetime.now(timezone.utc).isoformat()
    }


# ── Paradigm Shift 4: Cross-Goal Skill Transfer ───────────────────────────────

def update_goal_index(index_path: Path, state: dict) -> list:
    """
    Add the current goal and its best specification to the goal similarity index.
    """
    existing = json.loads(index_path.read_text()) if index_path.exists() else []

    goal = state.get("goal", "")
    if not goal:
        return existing

    spec = state.get("specification", {})
    perf = state.get("analysis", {}).get("performance_score", 0)
    align = state.get("analysis", {}).get("alignment", {}).get("alignment_score", 0)
    combined_score = round((perf + align) / 2, 4)

    # Check if this goal already exists in the index
    goal_hash = hashlib.sha256(goal.encode()).hexdigest()[:16]
    existing_entry = next((e for e in existing if e.get("goal_hash") == goal_hash), None)

    if existing_entry:
        # Update only if this cycle performed better
        if combined_score > existing_entry.get("best_score", 0):
            existing_entry["best_score"] = combined_score
            existing_entry["best_specification"] = spec
            existing_entry["best_cycle"] = state.get("cycle", 1)
            existing_entry["updated_at"] = datetime.now(timezone.utc).isoformat()
    else:
        existing.append({
            "goal_hash": goal_hash,
            "goal": goal,
            "keywords": list(_keywords(goal)),
            "best_score": combined_score,
            "best_specification": spec,
            "best_cycle": state.get("cycle", 1),
            "total_cycles": 1,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        })

    index_path.write_text(json.dumps(existing, indent=2))
    return existing


def find_transfer_match(new_goal: str, index: list, threshold: float = 0.60) -> Optional[dict]:
    """
    Find the best matching prior goal for cross-goal skill transfer.
    Returns the matching entry if similarity >= threshold, else None.
    """
    if not index:
        return None

    best_match = None
    best_score = 0.0

    for entry in index:
        sim = goal_similarity(new_goal, entry.get("goal", ""))
        if sim > best_score:
            best_score = sim
            best_match = entry

    if best_score >= threshold and best_match:
        return {
            "match_found": True,
            "similarity_score": best_score,
            "matched_goal": best_match.get("goal"),
            "matched_goal_hash": best_match.get("goal_hash"),
            "best_specification": best_match.get("best_specification"),
            "best_score": best_match.get("best_score"),
            "transfer_note": f"Bootstrapping from prior goal (similarity: {best_score:.2f}). Review and adjust criteria before running."
        }

    return {
        "match_found": False,
        "similarity_score": best_score,
        "matched_goal": best_match.get("goal") if best_match else None,
        "transfer_note": f"No match above threshold {threshold}. Starting fresh."
    }


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Unified Orchestrator Meta Learner")
    subparsers = parser.add_subparsers(dest="command")

    learn_parser = subparsers.add_parser("learn", help="Extract learnings from a completed cycle")
    learn_parser.add_argument("--state", required=True)
    learn_parser.add_argument("--output-dir", default=".")
    learn_parser.add_argument("--min-cycles", type=int, default=3)

    transfer_parser = subparsers.add_parser("transfer", help="Find a transfer match for a new goal")
    transfer_parser.add_argument("--goal", required=True)
    transfer_parser.add_argument("--index", required=True)
    transfer_parser.add_argument("--threshold", type=float, default=0.60)
    transfer_parser.add_argument("--output", default="transfer_result.json")

    index_parser = subparsers.add_parser("index-update", help="Update goal similarity index")
    index_parser.add_argument("--state", required=True)
    index_parser.add_argument("--index", required=True)

    args = parser.parse_args()

    if args.command == "learn":
        state = json.loads(Path(args.state).read_text())
        out = Path(args.output_dir)
        out.mkdir(parents=True, exist_ok=True)

        learning = extract_learnings(state)
        log_path = out / "learnings_log.json"
        all_learnings = update_learnings_log(log_path, learning)
        log(f"Learning recorded (id={learning['learning_id']}). Log now has {len(all_learnings)} entries.", "OK")

        patches = generate_patches(all_learnings, min_cycles=args.min_cycles)
        if patches["ready"]:
            patches_path = out / "meta_patches.json"
            patches_path.write_text(json.dumps(patches, indent=2))
            log(f"Meta patches generated: {len(patches['specification_patches'])} spec patches, {len(patches['rule_patches'])} rule patches", "OK")
        else:
            log(f"Meta patches not yet ready: {patches['reason']}", "INFO")

    elif args.command == "transfer":
        index = json.loads(Path(args.index).read_text()) if Path(args.index).exists() else []
        result = find_transfer_match(args.goal, index, threshold=args.threshold)
        Path(args.output).write_text(json.dumps(result, indent=2))
        if result["match_found"]:
            log(f"Transfer match found: '{result['matched_goal']}' (similarity: {result['similarity_score']:.2f})", "OK")
        else:
            log(f"No transfer match above threshold {args.threshold}. Best: {result['similarity_score']:.2f}", "INFO")

    elif args.command == "index-update":
        state = json.loads(Path(args.state).read_text())
        index_path = Path(args.index)
        updated = update_goal_index(index_path, state)
        log(f"Goal index updated. Now has {len(updated)} entries.", "OK")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
