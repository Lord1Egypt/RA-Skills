#!/usr/bin/env python3
"""Gate for the first runnable generic-skill lane.

Includes a 6-layer mechanical validation system that runs BEFORE the
keep/pending_promote/revert/reject decision logic.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from lib.common import (
    KEEP_CATEGORIES,
    SCHEMA_VERSION,
    protected_target,
    read_json,
    utc_now_iso,
    write_json,
)
from lib.state_machine import (
    DEFAULT_STATE_ROOT,
    append_pending_promote,
    append_veto,
    ensure_tree,
    make_receipt_path,
    restore_backup,
    update_state,
)


# ---------------------------------------------------------------------------
# 6-layer mechanical validation
# ---------------------------------------------------------------------------


class GateLayer:
    """Base class for gate validation layers."""

    def __init__(self, name: str, required: bool = True):
        self.name = name
        self.required = required

    def validate(self, candidate: dict, execution: dict | None = None) -> dict:
        """Returns {passed: bool, details: str, layer: str}"""
        raise NotImplementedError


class SchemaGate(GateLayer):
    """Layer 0: Validate JSON artifact structure."""

    def __init__(self):
        super().__init__("schema", required=True)

    def validate(self, candidate, execution=None):
        required_fields = ["id", "category", "risk_level", "execution_plan"]
        missing = [f for f in required_fields if f not in candidate]
        return {
            "passed": len(missing) == 0,
            "details": f"Missing: {missing}" if missing else "OK",
            "layer": self.name,
        }


class CompileGate(GateLayer):
    """Layer 1: Verify modified files are valid (py_compile for Python, basic checks for Markdown)."""

    def __init__(self):
        super().__init__("compile", required=True)

    def validate(self, candidate, execution=None):
        if not execution or not execution.get("result", {}).get("modified"):
            return {"passed": True, "details": "No file modified", "layer": self.name}
        target = execution.get("result", {}).get("rollback_pointer", {}).get("target_path", "")
        if target.endswith(".py"):
            import py_compile

            try:
                py_compile.compile(target, doraise=True)
                return {"passed": True, "details": "Python compile OK", "layer": self.name}
            except py_compile.PyCompileError as e:
                return {"passed": False, "details": str(e), "layer": self.name}
        # For markdown and other files, basic validation
        return {"passed": True, "details": "Non-Python file, skip compile check", "layer": self.name}


class LintGate(GateLayer):
    """Layer 2: Basic lint checks on modified content."""

    def __init__(self):
        super().__init__("lint", required=False)  # Advisory, not blocking

    def validate(self, candidate, execution=None):
        diff = execution.get("result", {}).get("diff", "") if execution else ""
        warnings = []
        # Check for common issues in the diff
        for line in diff.split("\n"):
            if line.startswith("+") and not line.startswith("+++"):
                if len(line) > 120:
                    warnings.append(f"Line too long ({len(line)} chars)")
                if "\t" in line and "    " in line:
                    warnings.append("Mixed tabs and spaces")
        passed = len(warnings) == 0
        return {
            "passed": passed,
            "details": "; ".join(warnings) if warnings else "OK",
            "layer": self.name,
        }


class RegressionGate(GateLayer):
    """Layer 3: Check that the change doesn't regress any dimension."""

    def __init__(self):
        super().__init__("regression", required=True)

    def validate(self, candidate, execution=None):
        # Check evaluator evidence for regression signals
        evidence = candidate.get("evaluator_evidence", {})
        if not evidence or not evidence.get("enabled"):
            return {"passed": True, "details": "No evaluator evidence available", "layer": self.name}
        verdict = evidence.get("verdict", "")
        if verdict == "reject":
            return {"passed": False, "details": "Evaluator verdict: reject", "layer": self.name}
        return {"passed": True, "details": f"Evaluator verdict: {verdict}", "layer": self.name}


class ReviewGate(GateLayer):
    """Layer 4: Check discriminator panel consensus + LLM judge verdict."""

    def __init__(self):
        super().__init__("review", required=True)

    def validate(self, candidate, execution=None):
        recommendation = candidate.get("recommendation", "hold")
        panel = candidate.get("panel_result", {})
        label = panel.get("cognitive_label", "")
        llm_verdict = candidate.get("llm_verdict", {})
        llm_decision = llm_verdict.get("decision", "")
        llm_confidence = llm_verdict.get("confidence", 0.0)

        # LLM judge hard reject
        if llm_decision == "reject":
            return {"passed": False, "details": "LLM judge: reject", "layer": self.name}

        # DISPUTED + LLM reject = definite fail (redundant guard)
        if label == "DISPUTED" and llm_decision == "reject":
            return {"passed": False, "details": "Panel disputed + LLM judge reject", "layer": self.name}

        if recommendation == "reject":
            return {"passed": False, "details": "Recommendation: reject", "layer": self.name}
        if label == "DISPUTED":
            return {"passed": False, "details": "Panel disputed — needs human review", "layer": self.name}

        # LLM conditional with high confidence: warn but pass
        if llm_decision == "conditional" and llm_confidence > 0.7:
            if recommendation == "accept_for_execution":
                return {
                    "passed": True,
                    "details": f"Accepted [{label}] (LLM conditional, confidence={llm_confidence:.2f})",
                    "layer": self.name,
                }

        if recommendation == "accept_for_execution":
            return {"passed": True, "details": f"Accepted [{label}]", "layer": self.name}
        return {"passed": False, "details": f"Recommendation: {recommendation}", "layer": self.name}


class DoubtGate(GateLayer):
    """Layer 5: Reject candidates with speculative/hedging language.

    Scans candidate title and description for words like "might", "could",
    "possibly", "perhaps" that indicate the proposer isn't confident the
    change will actually help. Candidates should provide evidence, not hopes.
    """

    HEDGING_WORDS_EN = (
        "might", "could", "possibly", "perhaps", "maybe",
        "potentially", "likely", "probably", "should help",
        "may improve", "consider", "worth trying",
    )
    HEDGING_WORDS_ZH = (
        "可能", "也许", "或许", "大概", "应该会", "试试看", "不确定",
    )
    # Threshold varies by category: prompt/workflow candidates legitimately
    # use words like "consider" and "should help", so they get a higher bar.
    CATEGORY_THRESHOLDS = {
        "docs": 2,
        "reference": 2,
        "guardrail": 2,
        "prompt": 4,      # prompt candidates often discuss tradeoffs
        "workflow": 4,
        "tests": 3,
        "code": 3,
    }
    DEFAULT_THRESHOLD = 3

    def __init__(self):
        super().__init__("doubt", required=True)

    def validate(self, candidate, execution=None):
        text = " ".join([
            candidate.get("title", ""),
            candidate.get("description", ""),
            candidate.get("proposed_change_summary", ""),
        ]).lower()

        hits = []
        for word in self.HEDGING_WORDS_EN + self.HEDGING_WORDS_ZH:
            if word in text:
                hits.append(word)

        category = candidate.get("category", "")
        threshold = self.CATEGORY_THRESHOLDS.get(category, self.DEFAULT_THRESHOLD)

        if len(hits) >= threshold:
            return {
                "passed": False,
                "details": f"Speculative language detected ({len(hits)} hits, threshold={threshold} "
                           f"for {category or 'unknown'} category: {', '.join(hits[:5])}). "
                           f"Provide evidence instead of hedging.",
                "layer": self.name,
            }
        return {"passed": True, "details": "OK", "layer": self.name}


class HumanReviewGate(GateLayer):
    """Layer 6 (optional): Request human review for non-trivial changes.

    When a candidate reaches this layer, it means all mechanical gates passed
    but the change is too risky for auto-keep. This layer:
    1. Creates a review request (writes a review receipt JSON)
    2. Returns pending=True so the orchestrator knows to wait
    3. Can be checked later for completion
    """

    def __init__(self):
        super().__init__("human_review", required=False)  # Advisory — doesn't block, but signals

    def validate(self, candidate, execution=None):
        # Check if this candidate needs human review
        category = candidate.get("category", "")
        risk = candidate.get("risk_level", "low")
        recommendation = candidate.get("recommendation", "")

        needs_review = (
            risk in ("medium", "high")
            or category in ("prompt", "workflow", "tests", "code")
            or recommendation == "hold"
        )

        if not needs_review:
            return {"passed": True, "details": "Auto-keep eligible", "layer": self.name, "needs_human": False}

        # Create a review request
        review_request = self._create_review_request(candidate, execution)
        return {
            "passed": True,  # Don't block — but signal that human review is needed
            "details": f"Human review requested: {review_request['request_id']}",
            "layer": self.name,
            "needs_human": True,
            "review_request": review_request,
        }

    def _create_review_request(self, candidate, execution=None):
        """Create a structured review request."""
        return {
            "request_id": f"review-{candidate.get('id', 'unknown')}",
            "candidate_id": candidate.get("id", ""),
            "category": candidate.get("category", ""),
            "risk_level": candidate.get("risk_level", ""),
            "title": candidate.get("title", ""),
            "description": candidate.get("proposed_change_summary", ""),
            "diff": execution.get("result", {}).get("diff", "") if execution else "",
            "status": "pending",
            "requested_at": None,  # Will be set by caller with utc_now_iso()
        }

    def check_review_status(self, review_request_path: Path) -> dict:
        """Check if a pending review has been completed."""
        if not review_request_path.exists():
            return {"completed": False, "reason": "request_not_found"}

        data = read_json(review_request_path)
        if data.get("status") == "completed":
            return {
                "completed": True,
                "decision": data.get("decision", "pending"),
                "reviewer": data.get("reviewer", "unknown"),
                "comments": data.get("comments", ""),
            }
        return {"completed": False, "reason": "still_pending"}


DEFAULT_GATE_LAYERS = [SchemaGate(), CompileGate(), LintGate(), RegressionGate(), ReviewGate(), DoubtGate(), HumanReviewGate()]


def run_gate_layers(
    candidate: dict,
    execution: dict | None,
    layers: list[GateLayer] | None = None,
) -> dict:
    """Run all gate layers sequentially. Stop on first required failure."""
    if layers is None:
        layers = DEFAULT_GATE_LAYERS
    results = []
    all_passed = True
    failed_at = None

    for layer in layers:
        result = layer.validate(candidate, execution)
        results.append(result)
        if not result["passed"]:
            if layer.required:
                all_passed = False
                failed_at = layer.name
                break
            # Non-required layers just warn

    return {
        "all_passed": all_passed,
        "failed_at": failed_at,
        "layer_results": results,
        "layers_run": len(results),
        "layers_total": len(layers),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply gate decision for generic-skill lane")
    parser.add_argument("--ranking", required=True, help="Ranking artifact JSON")
    parser.add_argument("--execution", required=True, help="Execution artifact JSON")
    parser.add_argument("--state-root", default=str(DEFAULT_STATE_ROOT))
    parser.add_argument("--output", default=None)
    parser.add_argument(
        "--layers",
        default=None,
        help="Comma-separated list of layer names to run (default: all). "
        "Available: schema,compile,lint,regression,review,human_review",
    )
    return parser.parse_args()


def select_layers(layer_names: str | None) -> list[GateLayer]:
    """Filter DEFAULT_GATE_LAYERS to only those whose name is in the comma-separated list."""
    if layer_names is None:
        return list(DEFAULT_GATE_LAYERS)
    requested = [n.strip() for n in layer_names.split(",") if n.strip()]
    available = {layer.name: layer for layer in DEFAULT_GATE_LAYERS}
    selected = []
    for name in requested:
        if name not in available:
            raise ValueError(f"Unknown gate layer: {name!r}. Available: {sorted(available)}")
        selected.append(available[name])
    return selected


def load_candidate(ranking_artifact: dict, candidate_id: str) -> dict:
    for candidate in ranking_artifact.get("scored_candidates", []):
        if candidate["id"] == candidate_id:
            return candidate
    raise KeyError(f"candidate not found in ranking artifact: {candidate_id}")


def maybe_restore(execution_artifact: dict) -> dict:
    result = execution_artifact.get("result", {})
    rollback = result.get("rollback_pointer")
    if not rollback or not result.get("modified"):
        return {"attempted": False, "success": False, "reason": "no modified file to restore"}
    backup_path = Path(rollback["backup_path"]).expanduser().resolve()
    target_path = Path(rollback["target_path"]).expanduser().resolve()
    restore_backup(backup_path, target_path)
    return {
        "attempted": True,
        "success": True,
        "backup_path": str(backup_path),
        "target_path": str(target_path),
    }


def _layer_failure_detail(verdict: dict) -> str:
    """Extract the failure detail string from the first failed required layer."""
    for r in verdict["layer_results"]:
        if not r["passed"]:
            return r["details"]
    return "unknown"


def _extract_human_review_signal(verdict: dict) -> dict | None:
    """If any layer returned needs_human=True, return the review request."""
    for r in verdict["layer_results"]:
        if r.get("needs_human"):
            return r.get("review_request")
    return None


def main() -> int:
    args = parse_args()
    state_root = Path(args.state_root).expanduser().resolve()
    ensure_tree(state_root)

    ranking_artifact = read_json(Path(args.ranking).expanduser().resolve())
    execution_artifact = read_json(Path(args.execution).expanduser().resolve())
    run_id = ranking_artifact["run_id"]
    candidate_id = execution_artifact["candidate_id"]
    candidate = load_candidate(ranking_artifact, candidate_id)
    execution_result = execution_artifact.get("result", {})

    # --- 6-layer mechanical validation (runs BEFORE decision logic) ---
    selected_layers = select_layers(args.layers)
    layer_verdict = run_gate_layers(candidate, execution_artifact, layers=selected_layers)

    recommendation = candidate.get("recommendation")

    # If any required layer fails, override to revert/reject immediately
    if not layer_verdict["all_passed"]:
        rollback_outcome = {"attempted": False, "success": False, "reason": "not_needed"}
        if execution_result.get("modified"):
            decision = "revert"
            rollback_outcome = maybe_restore(execution_artifact)
        else:
            decision = "reject"
        reason = f"gate layer '{layer_verdict['failed_at']}' failed: {_layer_failure_detail(layer_verdict)}"
    else:
        # --- Original 4-way decision logic (only reached if all required layers pass) ---
        category = candidate.get("category")
        target_path = candidate.get("target_path")
        keep_eligible = (
            recommendation == "accept_for_execution"
            and category in KEEP_CATEGORIES
            and candidate.get("risk_level") == "low"
            and not protected_target(target_path)
            and execution_result.get("status") in {"success", "no_change"}
        )

        rollback_outcome = {"attempted": False, "success": False, "reason": "not_needed"}
        reason = ""
        if keep_eligible:
            decision = "keep"
            reason = "low-risk docs/reference/guardrail candidate executed successfully"
        elif recommendation == "reject":
            decision = "revert" if execution_result.get("modified") else "reject"
            rollback_outcome = maybe_restore(execution_artifact)
            reason = "critic rejected candidate under conservative gate"
        elif recommendation == "hold":
            decision = "pending_promote"
            rollback_outcome = maybe_restore(execution_artifact)
            reason = "critic marked candidate as hold; persisted to pending_promote for later human/control-plane review"
        elif execution_result.get("status") == "unsupported":
            decision = "reject"
            reason = execution_result.get("reason", "executor returned unsupported")
        elif execution_result.get("status") not in {"success", "no_change"}:
            decision = "revert" if execution_result.get("modified") else "reject"
            rollback_outcome = maybe_restore(execution_artifact)
            reason = f"execution status `{execution_result.get('status')}` did not pass gate"
        else:
            decision = "pending_promote"
            rollback_outcome = maybe_restore(execution_artifact)
            reason = "candidate is not auto-keep eligible in first runnable version; escalated to pending_promote"

    # --- Human review escalation ---
    # If mechanical gates passed but human review layer flagged needs_human,
    # escalate keep → pending_promote so a human can approve.
    human_review_request = _extract_human_review_signal(layer_verdict) if layer_verdict["all_passed"] else None
    if human_review_request and decision == "keep":
        decision = "pending_promote"
        human_review_request["requested_at"] = utc_now_iso()
        reason = f"human review requested ({human_review_request['request_id']}); escalated from keep to pending_promote"
        rollback_outcome = maybe_restore(execution_artifact)

    # Attach category/target_path for receipt even when layers failed early
    category = candidate.get("category")
    target_path = candidate.get("target_path")

    output_path = Path(args.output).expanduser().resolve() if args.output else make_receipt_path(state_root, "gate", run_id, candidate_id)
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "lane": ranking_artifact.get("lane", "generic-skill"),
        "run_id": run_id,
        "stage": "gated",
        "status": "success",
        "created_at": utc_now_iso(),
        "decision": decision,
        "reason": reason,
        "candidate_id": candidate_id,
        "candidate_category": category,
        "source_ranking_artifact": args.ranking,
        "source_execution_artifact": args.execution,
        "rollback": rollback_outcome,
        "gate_layers": layer_verdict,
        "next_step": "propose_candidates" if decision == "keep" else "human_promote_review" if decision == "pending_promote" else "re-propose_or_manual_override",
        "next_owner": "proposer" if decision == "keep" else "human" if decision == "pending_promote" else "proposer",
        "truth_anchor": str(output_path),
    }
    if human_review_request:
        receipt["human_review_request"] = human_review_request
    write_json(output_path, receipt)

    if decision == "pending_promote":
        pending_entry = {
            "run_id": run_id,
            "candidate_id": candidate_id,
            "category": category,
            "target_path": target_path,
            "recommendation": recommendation,
            "receipt_path": str(output_path),
            "created_at": utc_now_iso(),
        }
        if human_review_request:
            pending_entry["human_review_request"] = human_review_request
            # Also write the review request to its own file for the review CLI
            review_dir = state_root / "state" / "reviews"
            review_dir.mkdir(parents=True, exist_ok=True)
            review_path = review_dir / f"{human_review_request['request_id']}.json"
            write_json(review_path, human_review_request)
        append_pending_promote(state_root, pending_entry)
    elif decision in {"reject", "revert"}:
        append_veto(
            state_root,
            {
                "run_id": run_id,
                "candidate_id": candidate_id,
                "category": category,
                "target_path": target_path,
                "decision": decision,
                "reason": reason,
                "receipt_path": str(output_path),
                "created_at": utc_now_iso(),
            },
        )

    update_state(
        state_root,
        run_id=run_id,
        stage={
            "keep": "gated_keep",
            "pending_promote": "gated_pending",
            "revert": "gated_revert",
            "reject": "gated_reject",
        }[decision],
        status=decision,
        target_path=ranking_artifact["target"]["path"],
        truth_anchor=str(output_path),
        extra={
            "candidate_id": candidate_id,
            "decision": decision,
            "receipt_path": str(output_path),
        },
    )
    print(str(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
