"""
Tests for Agent Integration

Covers:
- CMSExecutorClient permission checks
- Role-based permission matrix
- Quick execution methods (WordPress/Shopify/Amazon)
- Batch execution
- Preview mode
- MCP tools definitions
- GEO pipeline integration
- create_executor_for_agent factory
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cms_executor.connectors.base_connector import (
    CMSPlatform, CMSOperationType, CMSResourceType, CMSResult, CMSOperation, RiskLevel,
)
from cms_executor.agent_integration import (
    CMSExecutorClient,
    CMSExecutorTools,
    AgentRole,
    ROLE_PERMISSIONS,
    PermissionError,
    check_permission,
    require_permission,
    ExecutionResult,
    create_executor_for_agent,
)
from cms_executor.engine.executor import CMSTaskExecutor, ExecutionPlan, ExecutionStatus, ExecutionMode
from cms_executor.engine.approval import ApprovalWorkflow
from cms_executor.engine.audit import CMSAuditLogger


class MockConnector:
    """Mock connector for agent integration tests"""
    platform = CMSPlatform.WORDPRESS

    def __init__(self):
        pass

    async def connect(self): return True
    async def disconnect(self): pass
    async def health_check(self): return True

    async def read(self, resource_id: str) -> CMSResult:
        return CMSResult.ok(
            CMSOperation(platform=self.platform, operation_type=CMSOperationType.READ, resource_id=resource_id),
            resource_id=resource_id,
            data={"title": "Test Post", "content": "Hello World"},
        )

    async def update(self, resource_id: str, data: dict, resource_type=None) -> CMSResult:
        return CMSResult.ok(
            CMSOperation(platform=self.platform, operation_type=CMSOperationType.UPDATE, resource_id=resource_id),
            resource_id=resource_id,
            data=data,
        )

    async def create(self, data: dict, resource_type=None) -> CMSResult:
        return CMSResult.ok(
            CMSOperation(platform=self.platform, operation_type=CMSOperationType.CREATE),
            resource_id="new_456",
            data=data,
        )

    async def delete(self, resource_id: str, soft: bool = True) -> CMSResult:
        return CMSResult.ok(
            CMSOperation(platform=self.platform, operation_type=CMSOperationType.DELETE, resource_id=resource_id),
            resource_id=resource_id,
        )

    async def snapshot(self, resource_id: str) -> str:
        return f"snap_{resource_id}"

    @property
    def status(self):
        from cms_executor.connectors.base_connector import CMSConnectionStatus
        return CMSConnectionStatus.CONNECTED


# =============================================================================
# Tests: Role Permissions
# =============================================================================

class TestRolePermissions:
    def test_geo_analyst_read_write(self):
        assert check_permission(AgentRole.GEO_ANALYST, CMSPlatform.WORDPRESS, "read") is True
        assert check_permission(AgentRole.GEO_ANALYST, CMSPlatform.WORDPRESS, "write") is True
        assert check_permission(AgentRole.GEO_ANALYST, CMSPlatform.AMAZON, "write") is False

    def test_amazon_operator_amazon_write(self):
        assert check_permission(AgentRole.AMAZON_OPERATOR, CMSPlatform.AMAZON, "write") is True
        assert check_permission(AgentRole.AMAZON_OPERATOR, CMSPlatform.WORDPRESS, "write") is False

    def test_chief_rollback(self):
        assert check_permission(AgentRole.CHIEF_OF_STAFF, CMSPlatform.WORDPRESS, "write") is True
        assert ROLE_PERMISSIONS[AgentRole.CHIEF_OF_STAFF].get("rollback") is True

    def test_viewer_readonly(self):
        assert check_permission(AgentRole.VIEWER, CMSPlatform.WORDPRESS, "read") is True
        assert check_permission(AgentRole.VIEWER, CMSPlatform.WORDPRESS, "write") is False

    def test_admin_full_access(self):
        perms = ROLE_PERMISSIONS[AgentRole.ADMIN]
        assert perms.get("admin") is True
        assert perms.get("rollback") is True


# =============================================================================
# Tests: Permission Enforcement
# =============================================================================

class TestPermissionEnforcement:
    def test_require_permission_passes(self):
        # Should not raise
        require_permission(AgentRole.CONTENT_CREATOR, CMSPlatform.WORDPRESS, "write")

    def test_require_permission_fails(self):
        with pytest.raises(PermissionError) as exc_info:
            require_permission(AgentRole.VIEWER, CMSPlatform.WORDPRESS, "write")
        assert "does not have permission" in str(exc_info.value)


# =============================================================================
# Tests: CMSExecutorClient
# =============================================================================

class TestCMSExecutorClient:
    def setup_method(self):
        self.mock_conn = MockConnector()
        self.executor = CMSTaskExecutor(
            connectors={CMSPlatform.WORDPRESS: self.mock_conn},
            approval_workflow=ApprovalWorkflow(),
            audit_logger=CMSAuditLogger(enable_console=False),
        )

    @pytest.mark.asyncio
    async def test_read_allowed(self):
        client = CMSExecutorClient(agent_id="test_01", agent_role=AgentRole.VIEWER, executor=self.executor)
        result = await client.execute(platform="wordpress", operation="read", resource_id="posts/123")
        assert result.success is True
        assert result.data["results"][0]["data"]["title"] == "Test Post"

    @pytest.mark.asyncio
    async def test_write_denied_for_viewer(self):
        client = CMSExecutorClient(agent_id="test_01", agent_role=AgentRole.VIEWER, executor=self.executor)
        result = await client.execute(platform="wordpress", operation="update", resource_id="posts/123", data={"title": "New"})
        assert result.success is False
        assert "Permission" in result.message

    @pytest.mark.asyncio
    async def test_write_allowed_for_content_creator(self):
        client = CMSExecutorClient(agent_id="test_01", agent_role=AgentRole.CONTENT_CREATOR, executor=self.executor)
        result = await client.execute(platform="wordpress", operation="update", resource_id="posts/123", data={"title": "New Title"})
        assert result.success is True

    @pytest.mark.asyncio
    async def test_preview_only_mode(self):
        # GEO Analyst should be preview-only by default
        client = CMSExecutorClient(agent_id="geo_01", agent_role=AgentRole.GEO_ANALYST, executor=self.executor)
        result = await client.execute(platform="wordpress", operation="update", resource_id="posts/123", data={"title": "New"})
        # Should work but in preview mode
        assert result.success is True

    @pytest.mark.asyncio
    async def test_wordpress_seo_update(self):
        client = CMSExecutorClient(agent_id="geo_01", agent_role=AgentRole.GEO_ANALYST, executor=self.executor)
        result = await client.update_wordpress_seo(
            resource_id="posts/456",
            seo_data={"seo_title": "Optimized Title", "seo_description": "Meta description"},
        )
        assert result.success is True
        assert "SEO updated" in result.message

    @pytest.mark.asyncio
    async def test_preview_method(self):
        client = CMSExecutorClient(agent_id="test_01", agent_role=AgentRole.CONTENT_CREATOR, executor=self.executor)
        preview = await client.preview(
            platform="wordpress",
            operation="update",
            resource_id="posts/123",
            data={"title": "Preview Title"},
        )
        assert preview["success"] is True
        assert preview["would_execute"] is True

    @pytest.mark.asyncio
    async def test_batch_execute_parallel(self):
        client = CMSExecutorClient(agent_id="test_01", agent_role=AgentRole.CONTENT_CREATOR, executor=self.executor)
        ops = [
            {"platform": "wordpress", "operation": "read", "resource_id": f"posts/{i}"}
            for i in range(3)
        ]
        results = await client.batch_execute(ops, parallel=True)
        assert len(results) == 3
        assert all(r.success for r in results)

    @pytest.mark.asyncio
    async def test_unknown_platform(self):
        client = CMSExecutorClient(agent_id="test_01", agent_role=AgentRole.CONTENT_CREATOR, executor=self.executor)
        result = await client.execute(platform="nonexistent", operation="read", resource_id="x")
        assert result.success is False


# =============================================================================
# Tests: ExecutionResult
# =============================================================================

class TestExecutionResult:
    def test_from_context_success(self):
        from cms_executor.engine.executor import ExecutionContext
        ctx = ExecutionContext(
            execution_id="exec_123",
            plan_id="plan_456",
            status=ExecutionStatus.COMPLETED,
            results=[
                CMSResult.ok(
                    CMSOperation(platform=CMSPlatform.WORDPRESS, operation_type=CMSOperationType.READ, resource_id="posts/1"),
                    resource_id="posts/1",
                    data={"title": "Test"},
                )
            ]
        )
        result = ExecutionResult.from_context(ctx)
        assert result.success is True
        assert result.execution_id == "exec_123"
        assert result.resource_id == "posts/1"

    def test_from_context_failure(self):
        from cms_executor.engine.executor import ExecutionContext
        ctx = ExecutionContext(
            execution_id="exec_123",
            status=ExecutionStatus.FAILED,
            error="Validation failed",
        )
        result = ExecutionResult.from_context(ctx)
        assert result.success is False
        assert "Validation failed" in result.message


# =============================================================================
# Tests: CMSExecutorTools (MCP)
# =============================================================================

class TestCMSExecutorTools:
    def test_tools_definition(self):
        mock_conn = MockConnector()
        executor = CMSTaskExecutor(
            connectors={CMSPlatform.WORDPRESS: mock_conn},
            approval_workflow=ApprovalWorkflow(),
        )
        tools = CMSExecutorTools(executor, AgentRole.CONTENT_CREATOR)
        tool_defs = tools.tools
        assert len(tool_defs) == 5
        tool_names = [t["name"] for t in tool_defs]
        assert "cms_execute" in tool_names
        assert "cms_preview" in tool_names
        assert "cms_rollback" in tool_names
        assert "cms_health" in tool_names
        assert "cms_batch" in tool_names

    @pytest.mark.asyncio
    async def test_cms_health_tool(self):
        mock_conn = MockConnector()
        executor = CMSTaskExecutor(
            connectors={CMSPlatform.WORDPRESS: mock_conn},
        )
        tools = CMSExecutorTools(executor)
        result = await tools.call_tool("cms_health", {"platform": "wordpress"})
        assert result["success"] is True
        assert result["status"] == "connected"

    @pytest.mark.asyncio
    async def test_cms_execute_tool(self):
        mock_conn = MockConnector()
        executor = CMSTaskExecutor(
            connectors={CMSPlatform.WORDPRESS: mock_conn},
            approval_workflow=ApprovalWorkflow(),
        )
        tools = CMSExecutorTools(executor, AgentRole.CONTENT_CREATOR)
        result = await tools.call_tool("cms_execute", {
            "platform": "wordpress",
            "operation": "read",
            "resource_id": "posts/123",
        })
        assert result["success"] is True
        assert "data" in result

    @pytest.mark.asyncio
    async def test_unknown_tool(self):
        mock_conn = MockConnector()
        executor = CMSTaskExecutor(
            connectors={CMSPlatform.WORDPRESS: mock_conn},
        )
        tools = CMSExecutorTools(executor)
        result = await tools.call_tool("unknown_tool", {})
        assert result["success"] is False
        assert "Unknown tool" in result["message"]


# =============================================================================
# Tests: Factory Function
# =============================================================================

class TestFactory:
    def test_create_executor_for_agent(self):
        executor, client, tools = create_executor_for_agent(
            credentials={
                CMSPlatform.WORDPRESS: {
                    "api_base": "https://example.com/wp-json",
                    "api_key": "user:pass",
                },
            },
            agent_role="content_creator",
        )
        assert executor is not None
        assert client is not None
        assert tools is not None
        assert CMSPlatform.WORDPRESS in executor.connectors


# =============================================================================
# Tests: GEO Pipeline Integration
# =============================================================================

class TestGEOPipeline:
    @pytest.mark.asyncio
    async def test_geo_pipeline_integration(self):
        from cms_executor.agent_integration import integrate_with_geo_pipeline
        mock_conn = MockConnector()
        executor = CMSTaskExecutor(
            connectors={CMSPlatform.WORDPRESS: mock_conn},
            approval_workflow=ApprovalWorkflow(),
        )
        geo_insights = [
            {
                "type": "seo_update",
                "platform": "wordpress",
                "operation": "update",
                "resource_id": "posts/100",
                "data": {"seo_title": "Optimized for keywords", "seo_description": "Meta desc"},
            },
            {
                "type": "seo_update",
                "platform": "wordpress",
                "operation": "update",
                "resource_id": "posts/101",
                "data": {"seo_title": "Another optimized", "seo_description": "Meta desc 2"},
            },
        ]
        results = await integrate_with_geo_pipeline(geo_insights, executor, AgentRole.GEO_ANALYST)
        assert len(results) == 2
        assert all(r.success for r in results)
