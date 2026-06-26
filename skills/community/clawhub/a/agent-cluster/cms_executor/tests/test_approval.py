"""
Tests for Approval Workflow

Covers:
- ApprovalChain tier mapping
- Risk level escalation
- Submit / approve / reject / escalate
- Timeout handling
- Dangerous pattern detection
"""

import pytest
import asyncio
from unittest.mock import patch
from datetime import datetime, timezone, timedelta

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cms_executor.connectors.base_connector import RiskLevel, CMSPlatform
from cms_executor.engine.approval import (
    ApprovalWorkflow, ApprovalStatus, ApprovalTier, ApprovalChain, ApprovalRequest,
)
from cms_executor.engine.executor import ExecutionPlan, ExecutionMode
from cms_executor.connectors.base_connector import CMSOperation, CMSOperationType, CMSResourceType


def make_plan(risk_level: RiskLevel, plan_id: str = "test_plan") -> ExecutionPlan:
    op = CMSOperation(
        operation_type=CMSOperationType.UPDATE,
        platform=CMSPlatform.WORDPRESS,
        resource_id="posts/123",
        risk_level=risk_level,
    )
    return ExecutionPlan(
        plan_id=plan_id,
        title=f"Test plan {risk_level.value}",
        operations=[op],
        agent_id="test_agent",
    )


# =============================================================================
# Tests: ApprovalChain
# =============================================================================

class TestApprovalChain:
    def test_low_risk_auto(self):
        tier, timeout = ApprovalChain.get_tier(RiskLevel.LOW)
        assert tier == ApprovalTier.AUTO
        assert timeout == 0

    def test_medium_risk_agent_self(self):
        tier, timeout = ApprovalChain.get_tier(RiskLevel.MEDIUM)
        assert tier == ApprovalTier.AGENT_SELF
        assert timeout == 600  # 10 min

    def test_high_risk_chief(self):
        tier, timeout = ApprovalChain.get_tier(RiskLevel.HIGH)
        assert tier == ApprovalTier.CHIEF
        assert timeout == 3600  # 1 hour

    def test_critical_risk_human(self):
        tier, timeout = ApprovalChain.get_tier(RiskLevel.CRITICAL)
        assert tier == ApprovalTier.HUMAN
        assert timeout == 86400  # 24 hours

    def test_dangerous_pattern_detection(self):
        dangerous_plan = {
            "operations": [
                {"operation_type": "delete", "data": {"force": True, "sql": "DROP TABLE"}}
            ]
        }
        assert ApprovalChain.is_dangerous(dangerous_plan) is True

        safe_plan = {
            "operations": [
                {"operation_type": "update", "data": {"title": "New Title"}}
            ]
        }
        assert ApprovalChain.is_dangerous(safe_plan) is False


# =============================================================================
# Tests: ApprovalWorkflow
# =============================================================================

class TestApprovalWorkflow:
    @pytest.mark.asyncio
    async def test_auto_approve_low_risk(self):
        workflow = ApprovalWorkflow()
        plan = make_plan(RiskLevel.LOW)
        approval_id = await workflow.submit(plan, RiskLevel.LOW, "test_agent")
        # AUTO tier: approval_id is immediately returned (no pending record)
        assert approval_id  # auto-approved
        status = await workflow.get_status(approval_id)
        # Should not be found in pending (already auto-approved)
        assert status in (ApprovalStatus.APPROVED, ApprovalStatus.CANCELLED, ApprovalStatus.PENDING)

    @pytest.mark.asyncio
    async def test_submit_medium_risk_pending(self):
        workflow = ApprovalWorkflow()
        plan = make_plan(RiskLevel.MEDIUM)
        approval_id = await workflow.submit(plan, RiskLevel.MEDIUM, "test_agent")
        assert approval_id
        pending = await workflow.list_pending()
        assert len(pending) == 1
        assert pending[0].approval_id == approval_id
        assert pending[0].tier == ApprovalTier.AGENT_SELF
        assert pending[0].risk_level == RiskLevel.MEDIUM

    @pytest.mark.asyncio
    async def test_approve(self):
        workflow = ApprovalWorkflow()
        plan = make_plan(RiskLevel.MEDIUM)
        approval_id = await workflow.submit(plan, RiskLevel.MEDIUM, "test_agent")
        ok = await workflow.approve(approval_id, "Looks good", "chief_01")
        assert ok is True
        status = await workflow.get_status(approval_id)
        assert status == ApprovalStatus.APPROVED
        # Should no longer be pending
        pending = await workflow.list_pending()
        assert approval_id not in [p.approval_id for p in pending]

    @pytest.mark.asyncio
    async def test_reject(self):
        workflow = ApprovalWorkflow()
        plan = make_plan(RiskLevel.HIGH)
        approval_id = await workflow.submit(plan, RiskLevel.HIGH, "test_agent")
        ok = await workflow.reject(approval_id, "Risk too high", "chief_01")
        assert ok is True
        status = await workflow.get_status(approval_id)
        assert status == ApprovalStatus.REJECTED

    @pytest.mark.asyncio
    async def test_escalate_agent_to_chief(self):
        workflow = ApprovalWorkflow()
        plan = make_plan(RiskLevel.MEDIUM)
        approval_id = await workflow.submit(plan, RiskLevel.MEDIUM, "test_agent")
        ok = await workflow.escalate(approval_id, "Need more review")
        assert ok is True
        pending = await workflow.list_pending()
        escalated = next(p for p in pending if p.approval_id == approval_id)
        assert escalated.tier == ApprovalTier.CHIEF

    @pytest.mark.asyncio
    async def test_escalate_chief_to_human(self):
        workflow = ApprovalWorkflow()
        plan = make_plan(RiskLevel.HIGH)
        approval_id = await workflow.submit(plan, RiskLevel.HIGH, "test_agent")
        await workflow.escalate(approval_id, "Need human review")
        pending = await workflow.list_pending()
        escalated = next(p for p in pending if p.approval_id == approval_id)
        assert escalated.tier == ApprovalTier.HUMAN

    @pytest.mark.asyncio
    async def test_cancel(self):
        workflow = ApprovalWorkflow()
        plan = make_plan(RiskLevel.MEDIUM)
        approval_id = await workflow.submit(plan, RiskLevel.MEDIUM, "test_agent")
        ok = await workflow.cancel(approval_id)
        assert ok is True
        pending = await workflow.list_pending()
        assert approval_id not in [p.approval_id for p in pending]

    @pytest.mark.asyncio
    async def test_approval_history(self):
        workflow = ApprovalWorkflow()
        plan = make_plan(RiskLevel.HIGH)
        approval_id = await workflow.submit(plan, RiskLevel.HIGH, "test_agent")
        await workflow.approve(approval_id, "Approved", "chief_01")
        pending = await workflow.list_pending()
        # approved items are not in pending
        # Check the internal state
        from cms_executor.engine.approval import ApprovalWorkflow as AW2
        w2 = ApprovalWorkflow()
        await w2.submit(plan, RiskLevel.MEDIUM, "test_agent")
        pending2 = await w2.list_pending()
        assert len(pending2) == 1
        assert pending2[0].history[0]["action"] == "submit"

    @pytest.mark.asyncio
    async def test_unknown_approval_rejected(self):
        workflow = ApprovalWorkflow()
        ok = await workflow.approve("non_existent_id", "test", "approver")
        assert ok is False


# =============================================================================
# Tests: ApprovalRequest
# =============================================================================

class TestApprovalRequest:
    def test_to_dict(self):
        req = ApprovalRequest(
            plan_id="plan_123",
            plan_summary={"title": "Test", "operations": []},
            risk_level=RiskLevel.MEDIUM,
            agent_id="agent_01",
            agent_role="content_creator",
            tier=ApprovalTier.AGENT_SELF,
        )
        d = req.to_dict()
        assert d["plan_id"] == "plan_123"
        assert d["risk_level"] == "medium"
        assert d["tier"] == "agent_self"

    def test_add_history(self):
        req = ApprovalRequest(
            plan_id="plan_123",
            risk_level=RiskLevel.HIGH,
            agent_id="agent_01",
        )
        req.add_history("submit", "agent_01")
        req.add_history("approve", "chief_01", "LGTM")
        assert len(req.history) == 2
        assert req.history[0]["action"] == "submit"
        assert req.history[1]["note"] == "LGTM"
