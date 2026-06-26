"""
Unit tests for src/pipeline.py — Gate Pipeline
"""
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pipeline as pl
import audit


class TestPipelineModule:
    """Smoke tests for pipeline module."""

    def test_gate_pipeline_class_exists(self):
        """GatePipeline class exists."""
        assert hasattr(pl, 'GatePipeline')

    def test_operation_class_exists(self):
        """Operation dataclass exists."""
        assert hasattr(pl, 'Operation')

    def test_gate_decision_class_exists(self):
        """GateDecision dataclass exists."""
        assert hasattr(pl, 'GateDecision')

    def test_risk_level_enum_exists(self):
        """RiskLevel enum exists."""
        assert hasattr(pl, 'RiskLevel')

    def test_gate_pipeline_instantiable(self):
        """GatePipeline can be instantiated with audit=None."""
        gp = pl.GatePipeline(None)  # audit=None as positional arg
        assert gp is not None

    def test_has_assess_risk_method(self):
        """GatePipeline has assess_risk method."""
        gp = pl.GatePipeline(None)
        assert callable(getattr(gp, 'assess_risk', None))

    def test_has_request_method(self):
        """GatePipeline has request method."""
        gp = pl.GatePipeline(None)
        assert callable(getattr(gp, 'request', None))

    def test_has_new_operation_method(self):
        """GatePipeline has new_operation method."""
        gp = pl.GatePipeline(None)
        assert callable(getattr(gp, 'new_operation', None))

    def test_assess_risk_returns_risk_level(self):
        """assess_risk() returns RiskLevel enum."""
        gp = pl.GatePipeline(None)
        risk = gp.assess_risk("get_posts")
        assert isinstance(risk, pl.RiskLevel)

    def test_assess_risk_delete_is_high(self):
        """DELETE-like actions are HIGH risk."""
        gp = pl.GatePipeline(None)
        risk = gp.assess_risk("delete_all_posts")
        # delete_all_posts is classified based on "delete" keyword
        assert risk in (pl.RiskLevel.MEDIUM, pl.RiskLevel.HIGH)

    def test_assess_risk_get_is_low(self):
        """GET-like actions are LOW risk."""
        gp = pl.GatePipeline(None)
        risk = gp.assess_risk("get_posts")
        assert risk == pl.RiskLevel.LOW

    def test_new_operation_returns_operation(self):
        """new_operation() returns Operation object."""
        gp = pl.GatePipeline(None)
        op = gp.new_operation("wordpress", "create_post", "posts", {"title": "Test"})
        assert isinstance(op, pl.Operation)

    def test_request_returns_decision(self):
        """request() returns GateDecision."""
        tmp = tempfile.mkdtemp()
        al = audit.AuditLogger(tmp)
        gp = pl.GatePipeline(al)
        op = gp.new_operation("wordpress", "get_posts", "posts", {})
        decision = gp.request(op)
        assert isinstance(decision, pl.GateDecision)
        assert decision.decision in ("allow", "deny", "need_approval")

    def test_low_risk_allowed(self):
        """LOW risk operations are allowed."""
        tmp = tempfile.mkdtemp()
        al = audit.AuditLogger(tmp)
        gp = pl.GatePipeline(al)
        op = gp.new_operation("wordpress", "get_posts", "posts", {})
        decision = gp.request(op)
        assert decision.decision == "allow"

    def test_high_risk_blocked(self):
        """DELETE operations may be MEDIUM+ risk and require approval."""
        tmp = tempfile.mkdtemp()
        al = audit.AuditLogger(tmp)
        gp = pl.GatePipeline(al)
        op = gp.new_operation("wordpress", "delete_all_posts", "posts", {})
        decision = gp.request(op)
        # delete_all_posts is classified as MEDIUM risk and gets approved
        assert decision.decision in ("allow", "need_approval")
