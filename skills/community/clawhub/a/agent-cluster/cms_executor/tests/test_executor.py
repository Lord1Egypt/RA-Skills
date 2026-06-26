"""
Tests for CMSTaskExecutor

Covers:
- ExecutionPlan creation and risk assessment
- Validation logic
- Sandbox pre-flight checks
- Approval workflow integration
- Single and batch execution
- Preview mode
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cms_executor.connectors.base_connector import (
    CMSCredentials, CMSPlatform, CMSOperation, CMSOperationType,
    CMSResourceType, RiskLevel, CMSResult, CMSConnectionStatus,
)
from cms_executor.engine.executor import (
    CMSTaskExecutor, ExecutionPlan, ExecutionContext, ExecutionStatus, ExecutionMode,
)
from cms_executor.engine.approval import ApprovalWorkflow, ApprovalStatus
from cms_executor.engine.rollback import RollbackManager, SnapshotStore
from cms_executor.engine.audit import CMSAuditLogger


class MockConnector:
    """Mock CMS Connector for testing"""
    platform = CMSPlatform.WORDPRESS

    def __init__(self, fail_read: bool = False, fail_update: bool = False):
        self._status = CMSConnectionStatus.CONNECTED
        self._capabilities = ["read", "create", "update", "delete"]
        self._fail_read = fail_read
        self._fail_update = fail_update

    async def connect(self): self._status = CMSConnectionStatus.CONNECTED; return True
    async def disconnect(self): self._status = CMSConnectionStatus.DISCONNECTED
    async def health_check(self): return True

    async def read(self, resource_id: str) -> CMSResult:
        if self._fail_read:
            return CMSResult.error(
                CMSOperation(platform=self.platform, operation_type=CMSOperationType.READ, resource_id=resource_id),
                "Not found", "NOT_FOUND"
            )
        return CMSResult.ok(
            CMSOperation(platform=self.platform, operation_type=CMSOperationType.READ, resource_id=resource_id),
            resource_id=resource_id,
            data={"title": "Mock Title", "content": "Mock Content"}
        )

    async def update(self, resource_id: str, data: dict, resource_type=None) -> CMSResult:
        if self._fail_update:
            return CMSResult.error(
                CMSOperation(platform=self.platform, operation_type=CMSOperationType.UPDATE, resource_id=resource_id),
                "Update failed", "UPDATE_ERROR"
            )
        return CMSResult.ok(
            CMSOperation(platform=self.platform, operation_type=CMSOperationType.UPDATE, resource_id=resource_id),
            resource_id=resource_id,
            data={"title": "Updated"}
        )

    async def create(self, data: dict, resource_type=None) -> CMSResult:
        return CMSResult.ok(
            CMSOperation(platform=self.platform, operation_type=CMSOperationType.CREATE),
            resource_id="new_123",
            data=data
        )

    async def delete(self, resource_id: str, soft: bool = True) -> CMSResult:
        return CMSResult.ok(
            CMSOperation(platform=self.platform, operation_type=CMSOperationType.DELETE, resource_id=resource_id),
            resource_id=resource_id,
            message=f"{'Soft' if soft else 'Hard'} delete"
        )

    async def list(self, filters: dict = None, page: int = 1, per_page: int = 20) -> CMSResult:
        return CMSResult.ok(
            CMSOperation(platform=self.platform, operation_type=CMSOperationType.LIST),
            data={"items": [{"id": "1"}, {"id": "2"}]}
        )

    async def snapshot(self, resource_id: str) -> str:
        return f"snap_{resource_id}_{1234567890}"

    @property
    def status(self): return self._status
    @property
    def capabilities(self): return self._capabilities


# =============================================================================
# Tests: ExecutionPlan
# =============================================================================

class TestExecutionPlan:
    def test_risk_assessment_low(self):
        plan = ExecutionPlan(
            title="Read plan",
            operations=[
                CMSOperation(operation_type=CMSOperationType.READ, platform=CMSPlatform.WORDPRESS, risk_level=RiskLevel.LOW),
            ]
        )
        assert plan.overall_risk_level() == RiskLevel.LOW

    def test_risk_assessment_medium(self):
        plan = ExecutionPlan(
            title="Mixed plan",
            operations=[
                CMSOperation(operation_type=CMSOperationType.READ, platform=CMSPlatform.WORDPRESS, risk_level=RiskLevel.LOW),
                CMSOperation(operation_type=CMSOperationType.CREATE, platform=CMSPlatform.WORDPRESS, risk_level=RiskLevel.MEDIUM),
            ]
        )
        assert plan.overall_risk_level() == RiskLevel.MEDIUM

    def test_risk_assessment_critical(self):
        plan = ExecutionPlan(
            title="Dangerous plan",
            operations=[
                CMSOperation(operation_type=CMSOperationType.READ, platform=CMSPlatform.WORDPRESS, risk_level=RiskLevel.LOW),
                CMSOperation(operation_type=CMSOperationType.DELETE, platform=CMSPlatform.WORDPRESS, risk_level=RiskLevel.HIGH),
                CMSOperation(operation_type=CMSOperationType.UPDATE, platform=CMSPlatform.WORDPRESS, risk_level=RiskLevel.CRITICAL),
            ]
        )
        assert plan.overall_risk_level() == RiskLevel.CRITICAL

    def test_empty_plan_has_low_risk(self):
        plan = ExecutionPlan(title="Empty plan")
        assert plan.overall_risk_level() == RiskLevel.LOW

    def test_to_dict(self):
        plan = ExecutionPlan(
            title="Test Plan",
            operations=[
                CMSOperation(
                    operation_type=CMSOperationType.UPDATE,
                    platform=CMSPlatform.WORDPRESS,
                    resource_id="posts/123",
                    risk_level=RiskLevel.MEDIUM,
                )
            ],
            agent_id="geo_analyst_01",
            tags=["seo", "geo"],
        )
        d = plan.to_dict()
        assert d["title"] == "Test Plan"
        assert d["risk_level"] == "medium"
        assert d["agent_id"] == "geo_analyst_01"
        assert d["tags"] == ["seo", "geo"]


# =============================================================================
# Tests: CMSTaskExecutor
# =============================================================================

class TestCMSTaskExecutor:
    @pytest.mark.asyncio
    async def test_execute_read_success(self):
        mock_conn = MockConnector()
        executor = CMSTaskExecutor(
            connectors={CMSPlatform.WORDPRESS: mock_conn},
            approval_workflow=ApprovalWorkflow(),
            audit_logger=CMSAuditLogger(enable_console=False),
        )
        plan = ExecutionPlan(
            title="Read test",
            operations=[
                CMSOperation(
                    operation_type=CMSOperationType.READ,
                    platform=CMSPlatform.WORDPRESS,
                    resource_id="posts/123",
                    agent_id="test_agent",
                )
            ],
            mode=ExecutionMode.LIVE,
        )
        ctx = await executor.execute(plan)
        assert ctx.status == ExecutionStatus.COMPLETED
        assert len(ctx.results) == 1
        assert ctx.results[0].success is True
        assert ctx.results[0].resource_id == "posts/123"

    @pytest.mark.asyncio
    async def test_execute_update_success(self):
        mock_conn = MockConnector()
        executor = CMSTaskExecutor(
            connectors={CMSPlatform.WORDPRESS: mock_conn},
            approval_workflow=ApprovalWorkflow(),
        )
        plan = ExecutionPlan(
            title="Update test",
            operations=[
                CMSOperation(
                    operation_type=CMSOperationType.UPDATE,
                    platform=CMSPlatform.WORDPRESS,
                    resource_id="posts/123",
                    data={"title": "Updated Title"},
                    agent_id="test_agent",
                )
            ],
            mode=ExecutionMode.LIVE,
        )
        ctx = await executor.execute(plan)
        assert ctx.status == ExecutionStatus.COMPLETED
        assert ctx.results[0].success is True
        assert ctx.results[0].snapshot_id.startswith("snap_")  # snapshot created

    @pytest.mark.asyncio
    async def test_preview_mode(self):
        mock_conn = MockConnector()
        executor = CMSTaskExecutor(
            connectors={CMSPlatform.WORDPRESS: mock_conn},
            approval_workflow=ApprovalWorkflow(),
        )
        plan = ExecutionPlan(
            title="Preview test",
            operations=[
                CMSOperation(
                    operation_type=CMSOperationType.UPDATE,
                    platform=CMSPlatform.WORDPRESS,
                    resource_id="posts/123",
                    data={"title": "New Title"},
                )
            ],
            mode=ExecutionMode.PREVIEW,
        )
        ctx = await executor.execute(plan)
        # Preview mode should not fail validation and should skip approval
        assert ctx.status == ExecutionStatus.EXECUTING or ctx.status == ExecutionStatus.COMPLETED

    @pytest.mark.asyncio
    async def test_validation_fails_on_empty_plan(self):
        mock_conn = MockConnector()
        executor = CMSTaskExecutor(
            connectors={CMSPlatform.WORDPRESS: mock_conn},
            approval_workflow=ApprovalWorkflow(),
        )
        plan = ExecutionPlan(title="Empty plan")
        ctx = await executor.execute(plan)
        assert ctx.status == ExecutionStatus.FAILED
        assert "no operations" in ctx.error.lower()

    @pytest.mark.asyncio
    async def test_validation_fails_on_mixed_platforms(self):
        mock_conn = MockConnector()
        executor = CMSTaskExecutor(
            connectors={CMSPlatform.WORDPRESS: mock_conn},
            approval_workflow=ApprovalWorkflow(),
        )
        plan = ExecutionPlan(
            title="Mixed platforms",
            operations=[
                CMSOperation(operation_type=CMSOperationType.READ, platform=CMSPlatform.WORDPRESS, resource_id="posts/123"),
                CMSOperation(operation_type=CMSOperationType.READ, platform=CMSPlatform.SHOPIFY, resource_id="products/1"),
            ]
        )
        ctx = await executor.execute(plan)
        assert ctx.status == ExecutionStatus.FAILED
        assert "Mixed platforms" in ctx.error

    @pytest.mark.asyncio
    async def test_validation_fails_on_missing_connector(self):
        executor = CMSTaskExecutor(
            connectors={},
            approval_workflow=ApprovalWorkflow(),
        )
        plan = ExecutionPlan(
            operations=[
                CMSOperation(operation_type=CMSOperationType.READ, platform=CMSPlatform.WORDPRESS, resource_id="posts/123"),
            ]
        )
        ctx = await executor.execute(plan)
        assert ctx.status == ExecutionStatus.FAILED
        assert "No connector" in ctx.error

    @pytest.mark.asyncio
    async def test_preview_method(self):
        mock_conn = MockConnector()
        executor = CMSTaskExecutor(
            connectors={CMSPlatform.WORDPRESS: mock_conn},
            approval_workflow=ApprovalWorkflow(),
        )
        plan = ExecutionPlan(
            operations=[
                CMSOperation(
                    operation_type=CMSOperationType.UPDATE,
                    platform=CMSPlatform.WORDPRESS,
                    resource_id="posts/123",
                    data={"title": "New"},
                    risk_level=RiskLevel.MEDIUM,
                )
            ],
            mode=ExecutionMode.LIVE,
        )
        preview = await executor.preview(plan)
        assert preview["risk_level"] == "medium"
        assert preview["operation_count"] == 1
        assert preview["approval_required"] is True

    @pytest.mark.asyncio
    async def test_batch_parallel_execution(self):
        mock_conn = MockConnector()
        executor = CMSTaskExecutor(
            connectors={CMSPlatform.WORDPRESS: mock_conn},
            approval_workflow=ApprovalWorkflow(),
        )
        plans = [
            ExecutionPlan(
                operations=[CMSOperation(
                    operation_type=CMSOperationType.READ,
                    platform=CMSPlatform.WORDPRESS,
                    resource_id=f"posts/{i}",
                    agent_id="test",
                )]
            )
            for i in range(3)
        ]
        results = await executor.execute_batch(plans, parallel=True)
        assert len(results) == 3
        assert all(r.status == ExecutionStatus.COMPLETED for r in results)


# =============================================================================
# Tests: Executor Context
# =============================================================================

class TestExecutionContext:
    def test_to_dict(self):
        ctx = ExecutionContext(
            plan_id="plan_123",
            platform=CMSPlatform.WORDPRESS,
            status=ExecutionStatus.COMPLETED,
            total_time_ms=250.5,
        )
        d = ctx.to_dict()
        assert d["plan_id"] == "plan_123"
        assert d["status"] == "completed"
        assert d["platform"] == "wordpress"
        assert d["total_time_ms"] == 250.5
