#!/usr/bin/env python3
"""Tests for the 6-layer mechanical gate validation system (including human review)."""

from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
from pathlib import Path

import pytest

# The directory name has a hyphen, so we can't use normal Python imports.
# Load gate.py by file path instead.
_GATE_PY = Path(__file__).resolve().parents[1] / "scripts" / "gate.py"
_spec = importlib.util.spec_from_file_location("gate", _GATE_PY)
_gate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_gate)

CompileGate = _gate.CompileGate
GateLayer = _gate.GateLayer
HumanReviewGate = _gate.HumanReviewGate
LintGate = _gate.LintGate
RegressionGate = _gate.RegressionGate
ReviewGate = _gate.ReviewGate
SchemaGate = _gate.SchemaGate
run_gate_layers = _gate.run_gate_layers
select_layers = _gate.select_layers
_extract_human_review_signal = _gate._extract_human_review_signal


# ---------------------------------------------------------------------------
# Fixtures — reusable candidate / execution dicts
# ---------------------------------------------------------------------------


def _full_candidate(**overrides) -> dict:
    """A candidate dict that passes SchemaGate and ReviewGate by default."""
    base = {
        "id": "cand-001",
        "category": "docs",
        "risk_level": "low",
        "execution_plan": {"steps": []},
        "recommendation": "accept_for_execution",
        "panel_result": {"cognitive_label": "CONSENSUS"},
        "target_path": "skills/example/SKILL.md",
    }
    base.update(overrides)
    return base


def _execution(modified: bool = False, diff: str = "", target_path: str = "", status: str = "success") -> dict:
    result = {"modified": modified, "diff": diff, "status": status}
    if target_path:
        result["rollback_pointer"] = {"target_path": target_path, "backup_path": "", "method": "restore_backup_file"}
    return {"candidate_id": "cand-001", "result": result}


# ===================================================================
# Layer 0 — SchemaGate
# ===================================================================


class TestSchemaGate:
    def test_all_fields_present(self):
        gate = SchemaGate()
        result = gate.validate(_full_candidate())
        assert result["passed"] is True
        assert result["layer"] == "schema"
        assert result["details"] == "OK"

    def test_missing_one_field(self):
        candidate = _full_candidate()
        del candidate["execution_plan"]
        result = SchemaGate().validate(candidate)
        assert result["passed"] is False
        assert "execution_plan" in result["details"]

    def test_missing_multiple_fields(self):
        candidate = {"recommendation": "accept_for_execution"}
        result = SchemaGate().validate(candidate)
        assert result["passed"] is False
        assert "id" in result["details"]
        assert "category" in result["details"]

    def test_extra_fields_ignored(self):
        candidate = _full_candidate(extra_field="hello")
        result = SchemaGate().validate(candidate)
        assert result["passed"] is True


# ===================================================================
# Layer 1 — CompileGate
# ===================================================================


class TestCompileGate:
    def test_no_execution(self):
        result = CompileGate().validate(_full_candidate(), execution=None)
        assert result["passed"] is True
        assert "No file modified" in result["details"]

    def test_no_modification(self):
        exe = _execution(modified=False)
        result = CompileGate().validate(_full_candidate(), exe)
        assert result["passed"] is True

    def test_non_python_file(self):
        exe = _execution(modified=True, target_path="README.md")
        result = CompileGate().validate(_full_candidate(), exe)
        assert result["passed"] is True
        assert "Non-Python" in result["details"]

    def test_valid_python_file(self):
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write("x = 1 + 2\n")
            f.flush()
            tmp_path = f.name
        try:
            exe = _execution(modified=True, target_path=tmp_path)
            result = CompileGate().validate(_full_candidate(), exe)
            assert result["passed"] is True
            assert "compile OK" in result["details"]
        finally:
            os.unlink(tmp_path)

    def test_invalid_python_file(self):
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write("def broken(\n")  # syntax error
            f.flush()
            tmp_path = f.name
        try:
            exe = _execution(modified=True, target_path=tmp_path)
            result = CompileGate().validate(_full_candidate(), exe)
            assert result["passed"] is False
            assert result["layer"] == "compile"
        finally:
            os.unlink(tmp_path)


# ===================================================================
# Layer 2 — LintGate
# ===================================================================


class TestLintGate:
    def test_clean_diff(self):
        exe = _execution(diff="+short line\n+another")
        result = LintGate().validate(_full_candidate(), exe)
        assert result["passed"] is True

    def test_no_execution(self):
        result = LintGate().validate(_full_candidate(), execution=None)
        assert result["passed"] is True

    def test_long_line(self):
        long_line = "+" + "x" * 130
        exe = _execution(diff=long_line)
        result = LintGate().validate(_full_candidate(), exe)
        assert result["passed"] is False
        assert "too long" in result["details"]

    def test_mixed_tabs_spaces(self):
        exe = _execution(diff="+\tsome    mixed indentation")
        result = LintGate().validate(_full_candidate(), exe)
        assert result["passed"] is False
        assert "Mixed tabs" in result["details"]

    def test_header_lines_ignored(self):
        # Lines starting with +++ should be ignored (diff header)
        long_header = "+++" + "x" * 200
        exe = _execution(diff=long_header)
        result = LintGate().validate(_full_candidate(), exe)
        assert result["passed"] is True

    def test_lint_is_advisory(self):
        gate = LintGate()
        assert gate.required is False


# ===================================================================
# Layer 3 — RegressionGate
# ===================================================================


class TestRegressionGate:
    def test_no_evidence(self):
        result = RegressionGate().validate(_full_candidate())
        assert result["passed"] is True
        assert "No regression" in result["details"]

    def test_evidence_disabled(self):
        candidate = _full_candidate(evaluator_evidence={"enabled": False})
        result = RegressionGate().validate(candidate)
        assert result["passed"] is True

    def test_evidence_accept(self):
        candidate = _full_candidate(evaluator_evidence={"enabled": True, "verdict": "accept"})
        result = RegressionGate().validate(candidate)
        assert result["passed"] is True

    def test_evidence_reject(self):
        candidate = _full_candidate(evaluator_evidence={"enabled": True, "verdict": "reject"})
        result = RegressionGate().validate(candidate)
        assert result["passed"] is False
        assert "reject" in result["details"]


# ===================================================================
# Layer 4 — ReviewGate
# ===================================================================


class TestReviewGate:
    def test_accept_consensus(self):
        candidate = _full_candidate(
            recommendation="accept_for_execution",
            panel_result={"cognitive_label": "CONSENSUS"},
        )
        result = ReviewGate().validate(candidate)
        assert result["passed"] is True
        assert "CONSENSUS" in result["details"]

    def test_reject(self):
        candidate = _full_candidate(recommendation="reject")
        result = ReviewGate().validate(candidate)
        assert result["passed"] is False

    def test_disputed(self):
        candidate = _full_candidate(
            recommendation="accept_for_execution",
            panel_result={"cognitive_label": "DISPUTED"},
        )
        result = ReviewGate().validate(candidate)
        assert result["passed"] is False
        assert "disputed" in result["details"].lower()

    def test_hold_defaults_to_fail(self):
        candidate = _full_candidate(recommendation="hold")
        result = ReviewGate().validate(candidate)
        assert result["passed"] is False
        assert "hold" in result["details"]

    def test_no_recommendation_defaults_hold(self):
        candidate = _full_candidate()
        del candidate["recommendation"]
        result = ReviewGate().validate(candidate)
        assert result["passed"] is False


# ===================================================================
# run_gate_layers()
# ===================================================================


class TestRunGateLayers:
    def test_all_pass(self):
        candidate = _full_candidate()
        verdict = run_gate_layers(candidate, _execution())
        assert verdict["all_passed"] is True
        assert verdict["failed_at"] is None
        assert verdict["layers_run"] == 6
        assert verdict["layers_total"] == 6

    def test_first_required_failure_stops(self):
        # Schema fails (missing fields) -> stops immediately
        candidate = {"recommendation": "accept_for_execution"}
        verdict = run_gate_layers(candidate, _execution())
        assert verdict["all_passed"] is False
        assert verdict["failed_at"] == "schema"
        # Only schema ran before stopping
        assert verdict["layers_run"] == 1

    def test_non_required_failure_continues(self):
        """LintGate is not required — failure should not stop the pipeline."""
        long_line = "+" + "x" * 200
        exe = _execution(diff=long_line)
        candidate = _full_candidate()
        verdict = run_gate_layers(candidate, exe)
        # Lint fails but is not required, so pipeline continues
        assert verdict["all_passed"] is True
        lint_result = [r for r in verdict["layer_results"] if r["layer"] == "lint"][0]
        assert lint_result["passed"] is False

    def test_required_failure_after_non_required(self):
        """If a non-required layer fails AND a later required layer also fails, report the required one."""
        long_line = "+" + "x" * 200
        exe = _execution(diff=long_line)
        # Candidate that will fail ReviewGate (recommendation=reject)
        candidate = _full_candidate(recommendation="reject")
        verdict = run_gate_layers(candidate, exe)
        assert verdict["all_passed"] is False
        assert verdict["failed_at"] == "review"

    def test_custom_layers_subset(self):
        candidate = _full_candidate()
        layers = [SchemaGate(), LintGate()]
        verdict = run_gate_layers(candidate, _execution(), layers=layers)
        assert verdict["layers_total"] == 2
        assert verdict["layers_run"] == 2
        assert verdict["all_passed"] is True

    def test_empty_layers_list(self):
        verdict = run_gate_layers({}, None, layers=[])
        assert verdict["all_passed"] is True
        assert verdict["layers_run"] == 0


# ===================================================================
# select_layers()
# ===================================================================


class TestSelectLayers:
    def test_none_returns_all(self):
        layers = select_layers(None)
        assert len(layers) == 6

    def test_single_layer(self):
        layers = select_layers("schema")
        assert len(layers) == 1
        assert layers[0].name == "schema"

    def test_multiple_layers(self):
        layers = select_layers("schema,lint,review")
        assert [l.name for l in layers] == ["schema", "lint", "review"]

    def test_unknown_layer_raises(self):
        with pytest.raises(ValueError, match="Unknown gate layer"):
            select_layers("schema,bogus")

    def test_whitespace_handling(self):
        layers = select_layers(" schema , lint ")
        assert [l.name for l in layers] == ["schema", "lint"]


# ===================================================================
# Integration: layer failures override decision logic
# ===================================================================


class TestIntegrationLayerOverridesDecision:
    """Test that layer failures correctly override the 4-way decision to revert/reject."""

    def test_schema_failure_with_modified_file_gives_revert(self):
        """When schema fails and file was modified, decision should be revert."""
        candidate = {"recommendation": "accept_for_execution"}  # missing required fields
        exe = _execution(modified=True, status="success")
        # Run just schema layer
        verdict = run_gate_layers(candidate, exe, layers=[SchemaGate()])
        assert not verdict["all_passed"]
        # Simulate the decision logic from main()
        if not verdict["all_passed"]:
            if exe["result"].get("modified"):
                decision = "revert"
            else:
                decision = "reject"
        assert decision == "revert"

    def test_schema_failure_without_modification_gives_reject(self):
        candidate = {"recommendation": "accept_for_execution"}
        exe = _execution(modified=False, status="success")
        verdict = run_gate_layers(candidate, exe, layers=[SchemaGate()])
        assert not verdict["all_passed"]
        if not verdict["all_passed"]:
            if exe["result"].get("modified"):
                decision = "revert"
            else:
                decision = "reject"
        assert decision == "reject"

    def test_all_layers_pass_allows_keep(self):
        """A fully valid candidate with all layers passing should reach the keep decision."""
        candidate = _full_candidate()
        exe = _execution(modified=False, status="success")
        verdict = run_gate_layers(candidate, exe)
        assert verdict["all_passed"]

    def test_regression_rejection_overrides_accept(self):
        """Even if recommendation is accept, a regression gate failure should block."""
        candidate = _full_candidate(evaluator_evidence={"enabled": True, "verdict": "reject"})
        exe = _execution(modified=True, status="success")
        verdict = run_gate_layers(candidate, exe)
        assert not verdict["all_passed"]
        assert verdict["failed_at"] == "regression"


# ===================================================================
# GateLayer base class
# ===================================================================


class TestGateLayerBase:
    def test_validate_not_implemented(self):
        layer = GateLayer("test_layer")
        with pytest.raises(NotImplementedError):
            layer.validate({})

    def test_default_required(self):
        layer = GateLayer("test")
        assert layer.required is True

    def test_optional_layer(self):
        layer = GateLayer("test", required=False)
        assert layer.required is False


# ===================================================================
# Layer 5 — HumanReviewGate
# ===================================================================


class TestHumanReviewGate:
    def test_low_risk_docs_no_review_needed(self):
        """Low risk docs category should not need human review."""
        candidate = _full_candidate(category="docs", risk_level="low")
        gate = HumanReviewGate()
        result = gate.validate(candidate)
        assert result["passed"] is True
        assert result["needs_human"] is False
        assert "Auto-keep" in result["details"]

    def test_medium_risk_prompt_review_requested(self):
        """Medium risk prompt category should trigger human review."""
        candidate = _full_candidate(category="prompt", risk_level="medium")
        gate = HumanReviewGate()
        result = gate.validate(candidate)
        assert result["passed"] is True
        assert result["needs_human"] is True
        assert "review_request" in result
        assert result["review_request"]["request_id"] == "review-cand-001"

    def test_hold_recommendation_review_requested(self):
        """Hold recommendation should trigger human review regardless of risk."""
        candidate = _full_candidate(recommendation="hold", risk_level="low", category="docs")
        gate = HumanReviewGate()
        result = gate.validate(candidate)
        assert result["passed"] is True
        assert result["needs_human"] is True

    def test_high_risk_triggers_review(self):
        """High risk should trigger review even for docs category."""
        candidate = _full_candidate(risk_level="high", category="docs")
        gate = HumanReviewGate()
        result = gate.validate(candidate)
        assert result["needs_human"] is True

    def test_code_category_triggers_review(self):
        candidate = _full_candidate(category="code", risk_level="low")
        gate = HumanReviewGate()
        result = gate.validate(candidate)
        assert result["needs_human"] is True

    def test_workflow_category_triggers_review(self):
        candidate = _full_candidate(category="workflow", risk_level="low")
        gate = HumanReviewGate()
        result = gate.validate(candidate)
        assert result["needs_human"] is True

    def test_tests_category_triggers_review(self):
        candidate = _full_candidate(category="tests", risk_level="low")
        gate = HumanReviewGate()
        result = gate.validate(candidate)
        assert result["needs_human"] is True

    def test_is_advisory_not_required(self):
        gate = HumanReviewGate()
        assert gate.required is False

    def test_create_review_request_structure(self):
        """Verify _create_review_request returns all expected fields."""
        candidate = _full_candidate(
            id="cand-99",
            category="prompt",
            risk_level="medium",
            title="Improve greeting",
            proposed_change_summary="Add morning greeting variant",
        )
        exe = _execution(diff="+ hello world")
        gate = HumanReviewGate()
        req = gate._create_review_request(candidate, exe)
        assert req["request_id"] == "review-cand-99"
        assert req["candidate_id"] == "cand-99"
        assert req["category"] == "prompt"
        assert req["risk_level"] == "medium"
        assert req["title"] == "Improve greeting"
        assert req["description"] == "Add morning greeting variant"
        assert req["diff"] == "+ hello world"
        assert req["status"] == "pending"
        assert req["requested_at"] is None  # Set by caller

    def test_create_review_request_no_execution(self):
        """Review request with no execution should have empty diff."""
        candidate = _full_candidate(id="cand-42")
        gate = HumanReviewGate()
        req = gate._create_review_request(candidate, execution=None)
        assert req["diff"] == ""

    def test_check_review_status_not_found(self):
        gate = HumanReviewGate()
        result = gate.check_review_status(Path("/nonexistent/path.json"))
        assert result["completed"] is False
        assert result["reason"] == "request_not_found"

    def test_check_review_status_completed(self):
        import json
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
            json.dump(
                {"status": "completed", "decision": "approve", "reviewer": "alice", "comments": "LGTM"},
                f,
            )
            tmp_path = f.name
        try:
            gate = HumanReviewGate()
            result = gate.check_review_status(Path(tmp_path))
            assert result["completed"] is True
            assert result["decision"] == "approve"
            assert result["reviewer"] == "alice"
            assert result["comments"] == "LGTM"
        finally:
            os.unlink(tmp_path)

    def test_check_review_status_still_pending(self):
        import json
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
            json.dump({"status": "pending"}, f)
            tmp_path = f.name
        try:
            gate = HumanReviewGate()
            result = gate.check_review_status(Path(tmp_path))
            assert result["completed"] is False
            assert result["reason"] == "still_pending"
        finally:
            os.unlink(tmp_path)


# ===================================================================
# _extract_human_review_signal()
# ===================================================================


class TestExtractHumanReviewSignal:
    def test_no_human_review_layer(self):
        verdict = {"layer_results": [{"passed": True, "layer": "schema"}]}
        assert _extract_human_review_signal(verdict) is None

    def test_human_review_present_but_not_needed(self):
        verdict = {
            "layer_results": [
                {"passed": True, "layer": "schema"},
                {"passed": True, "layer": "human_review", "needs_human": False},
            ]
        }
        assert _extract_human_review_signal(verdict) is None

    def test_human_review_needed(self):
        req = {"request_id": "review-x"}
        verdict = {
            "layer_results": [
                {"passed": True, "layer": "schema"},
                {"passed": True, "layer": "human_review", "needs_human": True, "review_request": req},
            ]
        }
        assert _extract_human_review_signal(verdict) == req


# ===================================================================
# Integration: human review gate escalates keep → pending_promote
# ===================================================================


class TestIntegrationHumanReviewEscalation:
    """Test that when HumanReviewGate signals needs_human, keep→pending_promote."""

    def test_keep_escalated_when_human_review_needed(self):
        """A medium-risk prompt candidate that would otherwise keep should be escalated."""
        # Candidate that would pass all required gates
        candidate = _full_candidate(
            category="prompt",  # triggers human review
            risk_level="medium",  # also triggers human review
        )
        exe = _execution(modified=False, status="success")
        # Run all layers
        verdict = run_gate_layers(candidate, exe)
        assert verdict["all_passed"] is True
        # The human review layer should signal needs_human
        human_req = _extract_human_review_signal(verdict)
        assert human_req is not None
        assert human_req["request_id"] == "review-cand-001"

    def test_low_risk_docs_no_escalation(self):
        """Low-risk docs should not trigger human review signal."""
        candidate = _full_candidate(category="docs", risk_level="low")
        exe = _execution(modified=False, status="success")
        verdict = run_gate_layers(candidate, exe)
        assert verdict["all_passed"] is True
        human_req = _extract_human_review_signal(verdict)
        assert human_req is None
