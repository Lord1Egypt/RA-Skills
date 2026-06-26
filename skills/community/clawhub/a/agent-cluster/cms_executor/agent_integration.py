"""
CMS Executor Agent Integration — Agent 调用接口

让现有 30 个 Agent 能够调用 CMS 执行能力：
1. CMSExecutorClient — Agent 的 SDK 客户端
2. CMSExecutorTools — MCP 协议暴露的工具集
3. 与 MCP GEO 连接器集成

使用方式：
  from agent_integration import CMSExecutorClient, create_executor_for_agent

  # Content Creator Agent
  client = CMSExecutorClient(agent_id="content_creator_01", agent_role="content_creator")
  result = await client.execute_wordpress(
      operation="update_post",
      resource_id="posts/123",
      data={"content": "New SEO optimized content..."}
  )
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from .connectors.base_connector import (
    BaseCMSConnector,
    CMSCredentials,
    CMSPlatform,
    CMSOperation,
    CMSOperationType,
    CMSResourceType,
    RiskLevel,
    CMSResult,
    CMSResource,
)
from .connectors import (
    WordPressConnector,
    ShopifyConnector,
    AmazonConnector,
    MagentoConnector,
)
from .engine import (
    CMSTaskExecutor,
    ExecutionPlan,
    ExecutionContext,
    ExecutionStatus,
    ExecutionMode,
    ApprovalWorkflow,
    RollbackManager,
    CMSAuditLogger,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# Agent 角色定义
# =============================================================================

class AgentRole(Enum):
    """Agent 角色枚举"""
    GEO_ANALYST = "geo_analyst"
    CONTENT_CREATOR = "content_creator"
    AMAZON_OPERATOR = "amazon_operator"
    FINANCE_AGENT = "finance_agent"
    CHIEF_OF_STAFF = "chief_of_staff"
    ADMIN = "admin"
    VIEWER = "viewer"


# Agent 角色 → CMS 权限映射
ROLE_PERMISSIONS: dict[AgentRole, dict[str, bool]] = {
    AgentRole.GEO_ANALYST: {
        "wordpress:read": True, "wordpress:write": True,
        "shopify:read": True, "shopify:write": True,
        "amazon:read": True, "amazon:write": False,
        "magento:read": True, "magento:write": True,
        "preview_only": True,  # GEO Analyst 默认只预览
    },
    AgentRole.CONTENT_CREATOR: {
        "wordpress:read": True, "wordpress:write": True,
        "shopify:read": True, "shopify:write": True,
        "amazon:read": True, "amazon:write": False,
        "magento:read": True, "magento:write": True,
        "preview_only": False,
    },
    AgentRole.AMAZON_OPERATOR: {
        "wordpress:read": True, "wordpress:write": False,
        "shopify:read": True, "shopify:write": False,
        "amazon:read": True, "amazon:write": True,
        "magento:read": False, "magento:write": False,
        "preview_only": False,
    },
    AgentRole.FINANCE_AGENT: {
        "wordpress:read": True, "wordpress:write": False,
        "shopify:read": True, "shopify:write": False,
        "amazon:read": True, "amazon:write": True,  # 价格调整
        "magento:read": True, "magento:write": True,  # 价格调整
        "preview_only": False,
    },
    AgentRole.CHIEF_OF_STAFF: {
        "wordpress:read": True, "wordpress:write": True,
        "shopify:read": True, "shopify:write": True,
        "amazon:read": True, "amazon:write": True,
        "magento:read": True, "magento:write": True,
        "rollback": True,  # 独有权限
        "preview_only": False,
    },
    AgentRole.ADMIN: {
        "wordpress:read": True, "wordpress:write": True,
        "shopify:read": True, "shopify:write": True,
        "amazon:read": True, "amazon:write": True,
        "magento:read": True, "magento:write": True,
        "rollback": True, "admin": True,
        "preview_only": False,
    },
    AgentRole.VIEWER: {
        "wordpress:read": True, "wordpress:write": False,
        "shopify:read": True, "shopify:write": False,
        "amazon:read": True, "amazon:write": False,
        "magento:read": True, "magento:write": False,
        "preview_only": True,
    },
}


# =============================================================================
# 权限检查
# =============================================================================

class PermissionError(Exception):
    """权限不足异常"""
    pass


def check_permission(role: AgentRole, platform: CMSPlatform, operation: str) -> bool:
    """检查 Agent 是否有权执行指定操作"""
    perms = ROLE_PERMISSIONS.get(role, {})
    key = f"{platform.value}:{operation}"
    return perms.get(key, False)


def require_permission(role: AgentRole, platform: CMSPlatform, operation: str) -> None:
    """权限检查，不通过则抛出 PermissionError"""
    if not check_permission(role, platform, operation):
        raise PermissionError(
            f"Agent role '{role.value}' does not have permission for "
            f"{platform.value}:{operation}"
        )


# =============================================================================
# CMS Executor Client
# =============================================================================

@dataclass
class ExecutionResult:
    """Agent 视角的执行结果（简化包装）"""
    success: bool
    message: str
    resource_id: str = ""
    data: dict = field(default_factory=dict)
    execution_id: str = ""
    preview_url: str = ""  # 预览模式下的模拟 URL

    @classmethod
    def from_context(cls, ctx: ExecutionContext) -> "ExecutionResult":
        first_result = ctx.results[0] if ctx.results else None
        return cls(
            success=ctx.status == ExecutionStatus.COMPLETED,
            message=ctx.error or "Execution completed",
            resource_id=first_result.resource_id if first_result else "",
            data={"results": [r.to_dict() for r in ctx.results]},
            execution_id=ctx.execution_id,
        )


class CMSExecutorClient:
    """
    Agent 视角的 CMS 执行客户端
    
    提供面向 Agent 的简洁 API，自动处理：
    - 权限验证
    - 执行模式（PREVIEW vs LIVE）
    - 平台路由
    - 审计追踪
    """

    def __init__(
        self,
        agent_id: str,
        agent_role: str | AgentRole = "viewer",
        executor: CMSTaskExecutor | None = None,
        audit_logger: CMSAuditLogger | None = None,
    ):
        self.agent_id = agent_id
        self.agent_role = agent_role if isinstance(agent_role, AgentRole) else AgentRole(agent_role)
        self.executor = executor
        self.audit_logger = audit_logger or CMSAuditLogger()
        self._session_id = str(uuid.uuid4())

    def _build_execution_plan(
        self,
        platform: CMSPlatform,
        operation_type: CMSOperationType,
        resource_id: str = "",
        data: dict = None,
        resource_type: CMSResourceType = CMSResourceType.POST,
        mode: ExecutionMode = ExecutionMode.LIVE,
        **kwargs,
    ) -> ExecutionPlan:
        """构建执行计划"""
        # 根据角色决定执行模式
        perms = ROLE_PERMISSIONS.get(self.agent_role, {})
        if perms.get("preview_only", False):
            mode = ExecutionMode.PREVIEW

        op = CMSOperation(
            operation_type=operation_type,
            resource_type=resource_type,
            platform=platform,
            resource_id=resource_id,
            data=data or {},
            agent_id=self.agent_id,
            execution_id=self._session_id,
            risk_level=self._estimate_risk(operation_type, platform),
        )
        return ExecutionPlan(
            operations=[op],
            mode=mode,
            agent_id=self.agent_id,
            agent_role=self.agent_role.value,
            title=kwargs.get("title", f"{operation_type.value} on {platform.value}"),
            description=kwargs.get("description", ""),
            tags=kwargs.get("tags", []),
        )

    def _estimate_risk(self, op_type: CMSOperationType, platform: CMSPlatform) -> RiskLevel:
        """估算操作风险"""
        if op_type == CMSOperationType.DELETE:
            return RiskLevel.HIGH
        if op_type in (CMSOperationType.CREATE, CMSOperationType.UPDATE):
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    # ── 统一执行入口 ─────────────────────────────────────────────────────

    async def execute(
        self,
        platform: str,
        operation: str,
        resource_id: str = "",
        data: dict = None,
        resource_type: str = "post",
        preview_only: bool = False,
        **kwargs,
    ) -> ExecutionResult:
        """
        统一的执行入口（Agent 主要调用此方法）
        
        Args:
            platform: "wordpress" | "shopify" | "amazon" | "magento"
            operation: "read" | "create" | "update" | "delete" | "list"
            resource_id: 资源 ID
            data: 操作数据
            resource_type: "post" | "page" | "product" | "order" | "inventory"
            preview_only: True=仅预览
        """
        try:
            cms_platform = CMSPlatform(platform)
            op_type = CMSOperationType(operation)
            res_type = CMSResourceType(resource_type)

            # 权限检查
            op_perm = "write" if op_type in (CMSOperationType.CREATE, CMSOperationType.UPDATE, CMSOperationType.DELETE) else "read"
            require_permission(self.agent_role, cms_platform, op_perm)

            if self.executor is None:
                return ExecutionResult(success=False, message="Executor not initialized")

            plan = self._build_execution_plan(
                platform=cms_platform,
                operation_type=op_type,
                resource_id=resource_id,
                data=data,
                resource_type=res_type,
                mode=ExecutionMode.PREVIEW if preview_only else ExecutionMode.LIVE,
                **kwargs,
            )
            ctx = await self.executor.execute(plan)
            return ExecutionResult.from_context(ctx)

        except PermissionError as e:
            logger.warning(f"[cms_client] Permission denied for {self.agent_id}: {e}")
            return ExecutionResult(success=False, message=str(e))
        except Exception as e:
            logger.exception(f"[cms_client] Execution error: {e}")
            return ExecutionResult(success=False, message=str(e))

    # ── WordPress 专属方法 ───────────────────────────────────────────────

    async def execute_wordpress(
        self,
        operation: str,
        resource_id: str = "",
        data: dict = None,
        preview_only: bool = False,
        **kwargs,
    ) -> ExecutionResult:
        """WordPress 操作"""
        result = await self.execute(
            platform="wordpress",
            operation=operation,
            resource_id=resource_id,
            data=data,
            resource_type=kwargs.get("resource_type", "post"),
            preview_only=preview_only,
            **kwargs,
        )
        # 预览模式生成预览 URL
        if preview_only and result.success:
            result.preview_url = f"https://preview.example.com/wp/{resource_id or 'new'}"
        return result

    async def update_wordpress_seo(
        self,
        resource_id: str,
        seo_data: dict,
        **kwargs,
    ) -> ExecutionResult:
        """WordPress SEO 更新（GEO 场景核心方法）"""
        result = await self.execute(
            platform="wordpress",
            operation="update",
            resource_id=resource_id,
            data=seo_data,
            resource_type="post",
            **kwargs,
        )
        if result.success:
            result.message = f"SEO updated for WordPress {resource_id}"
        return result

    # ── Shopify 专属方法 ─────────────────────────────────────────────────

    async def execute_shopify(
        self,
        operation: str,
        resource_id: str = "",
        data: dict = None,
        preview_only: bool = False,
        **kwargs,
    ) -> ExecutionResult:
        """Shopify 操作"""
        return await self.execute(
            platform="shopify",
            operation=operation,
            resource_id=resource_id,
            data=data,
            resource_type=kwargs.get("resource_type", "product"),
            preview_only=preview_only,
            **kwargs,
        )

    async def update_shopify_inventory(
        self,
        variant_id: str,
        quantity: int,
        **kwargs,
    ) -> ExecutionResult:
        """Shopify 库存更新"""
        require_permission(self.agent_role, CMSPlatform.SHOPIFY, "write")
        if self.executor is None:
            return ExecutionResult(success=False, message="Executor not initialized")
        from .connectors import ShopifyConnector
        connector = self.executor.connectors.get(CMSPlatform.SHOPIFY)
        if connector:
            result = await connector.update_inventory(variant_id, quantity)
            return ExecutionResult(
                success=result.success,
                message=result.message,
                resource_id=variant_id,
                data=result.data,
            )
        return ExecutionResult(success=False, message="Shopify connector not available")

    # ── Amazon 专属方法 ──────────────────────────────────────────────────

    async def execute_amazon(
        self,
        operation: str,
        resource_id: str = "",
        data: dict = None,
        preview_only: bool = False,
        **kwargs,
    ) -> ExecutionResult:
        """Amazon SP-API 操作"""
        return await self.execute(
            platform="amazon",
            operation=operation,
            resource_id=resource_id,
            data=data,
            resource_type=kwargs.get("resource_type", "product"),
            preview_only=preview_only,
            **kwargs,
        )

    async def update_amazon_price(
        self,
        asin: str,
        price: float,
        currency: str = "USD",
        **kwargs,
    ) -> ExecutionResult:
        """Amazon 价格更新"""
        require_permission(self.agent_role, CMSPlatform.AMAZON, "write")
        if self.executor is None:
            return ExecutionResult(success=False, message="Executor not initialized")
        connector = self.executor.connectors.get(CMSPlatform.AMAZON)
        if connector:
            result = await connector.update_pricing(asin, price, currency)
            return ExecutionResult(
                success=result.success,
                message=result.message,
                resource_id=asin,
                data=result.data,
            )
        return ExecutionResult(success=False, message="Amazon connector not available")

    # ── 批量操作 ─────────────────────────────────────────────────────────

    async def batch_execute(
        self,
        operations: list[dict],
        parallel: bool = True,
    ) -> list[ExecutionResult]:
        """
        批量执行多个操作
        
        operations 格式:
        [
            {"platform": "wordpress", "operation": "update", "resource_id": "posts/1", "data": {...}},
            {"platform": "shopify", "operation": "update_inventory", "resource_id": "gid://...", "data": {"quantity": 100}},
        ]
        """
        tasks = [self.execute(**op) for op in operations]
        if parallel:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return [r if isinstance(r, ExecutionResult) else ExecutionResult(success=False, message=str(r)) for r in results]
        else:
            results = []
            for task in tasks:
                results.append(await task)
            return results

    # ── 预览 ─────────────────────────────────────────────────────────────

    async def preview(
        self,
        platform: str,
        operation: str,
        resource_id: str = "",
        data: dict = None,
        **kwargs,
    ) -> dict:
        """
        预览执行效果（不实际执行）
        
        用于 Agent 在执行前确认效果。
        """
        result = await self.execute(
            platform=platform,
            operation=operation,
            resource_id=resource_id,
            data=data,
            preview_only=True,
            **kwargs,
        )
        return {
            "success": True,
            "preview": result.data,
            "message": "Preview mode - no actual changes made",
            "would_execute": True,
        }

    # ── 回滚 ─────────────────────────────────────────────────────────────

    async def rollback(
        self,
        snapshot_id: str,
    ) -> dict:
        """回滚到指定快照"""
        if self.agent_role not in (AgentRole.CHIEF_OF_STAFF, AgentRole.ADMIN):
            raise PermissionError(f"Role {self.agent_role.value} cannot perform rollback")

        if self.executor is None:
            return {"success": False, "message": "Executor not initialized"}

        rollback_manager = self.executor.rollback_manager
        connector = None  # 需要知道平台才能找到 connector
        result = await rollback_manager.rollback(snapshot_id, connector)
        return result.to_dict()


# =============================================================================
# MCP 工具集（暴露给 MCP Gateway）
# =============================================================================

class CMSExecutorTools:
    """
    MCP 协议暴露的 CMS 工具集
    
    每个方法对应一个 MCP 工具，Agent 通过 MCP 调用。
    """

    def __init__(self, executor: CMSTaskExecutor, agent_role: AgentRole = AgentRole.VIEWER):
        self.executor = executor
        self.client = CMSExecutorClient(
            agent_id="mcp_caller",
            agent_role=agent_role,
            executor=executor,
        )

    # ── MCP 工具定义 ─────────────────────────────────────────────────────

    @property
    def tools(self) -> list[dict]:
        """返回 MCP 工具定义"""
        return [
            {
                "name": "cms_execute",
                "description": "Execute a CMS operation (create, update, delete) on a platform",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "platform": {"type": "string", "enum": ["wordpress", "shopify", "amazon", "magento"]},
                        "operation": {"type": "string", "enum": ["read", "create", "update", "delete", "list"]},
                        "resource_id": {"type": "string", "description": "Resource ID (optional for create)"},
                        "data": {"type": "object", "description": "Operation payload"},
                        "resource_type": {"type": "string", "enum": ["post", "page", "product", "order", "inventory"]},
                    },
                    "required": ["platform", "operation"],
                },
            },
            {
                "name": "cms_preview",
                "description": "Preview a CMS operation without executing it",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "platform": {"type": "string", "enum": ["wordpress", "shopify", "amazon", "magento"]},
                        "operation": {"type": "string"},
                        "resource_id": {"type": "string"},
                        "data": {"type": "object"},
                    },
                    "required": ["platform", "operation"],
                },
            },
            {
                "name": "cms_rollback",
                "description": "Rollback a resource to a previous snapshot",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "snapshot_id": {"type": "string", "description": "Snapshot ID to rollback to"},
                    },
                    "required": ["snapshot_id"],
                },
            },
            {
                "name": "cms_health",
                "description": "Check health of a CMS platform connection",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "platform": {"type": "string", "enum": ["wordpress", "shopify", "amazon", "magento"]},
                    },
                    "required": ["platform"],
                },
            },
            {
                "name": "cms_batch",
                "description": "Execute multiple CMS operations in batch",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "operations": {"type": "array", "description": "List of CMS operations"},
                        "parallel": {"type": "boolean", "default": True},
                    },
                    "required": ["operations"],
                },
            },
        ]

    async def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """MCP 工具调用入口"""
        try:
            if tool_name == "cms_execute":
                result = await self.client.execute(**arguments)
                return {"success": result.success, "data": result.data, "message": result.message}
            elif tool_name == "cms_preview":
                result = await self.client.preview(**arguments)
                return result
            elif tool_name == "cms_rollback":
                result = await self.client.rollback(snapshot_id=arguments["snapshot_id"])
                return result
            elif tool_name == "cms_health":
                platform = CMSPlatform(arguments["platform"])
                connector = self.executor.connectors.get(platform)
                if connector:
                    ok = await connector.health_check()
                    return {"success": ok, "platform": arguments["platform"], "status": "connected" if ok else "disconnected"}
                return {"success": False, "message": f"No connector for {arguments['platform']}"}
            elif tool_name == "cms_batch":
                results = await self.client.batch_execute(
                    operations=arguments["operations"],
                    parallel=arguments.get("parallel", True),
                )
                return {"success": True, "results": [r.__dict__ for r in results]}
            else:
                return {"success": False, "message": f"Unknown tool: {tool_name}"}
        except PermissionError as e:
            return {"success": False, "message": f"Permission denied: {e}", "error_type": "PERMISSION_DENIED"}
        except Exception as e:
            logger.exception(f"[mcp_tools] Tool call failed: {e}")
            return {"success": False, "message": str(e)}


# =============================================================================
# 工厂函数
# =============================================================================

def create_executor_for_agent(
    credentials: dict[CMSPlatform, dict],
    agent_role: str = "viewer",
) -> tuple[CMSTaskExecutor, CMSExecutorClient, CMSExecutorTools]:
    """
    为指定 Agent 角色创建执行器
    
    Usage:
        executor, client, tools = create_executor_for_agent(
            credentials={
                CMSPlatform.WORDPRESS: {"api_base": "https://example.com/wp-json", "api_key": "..."},
                CMSPlatform.SHOPIFY: {"api_base": "https://example.myshopify.com/admin/api", "oauth_token": "..."},
            },
            agent_role="content_creator",
        )
    """
    creds_map: dict[CMSPlatform, CMSCredentials] = {}
    for platform, creds_data in credentials.items():
        creds_map[platform] = CMSCredentials.from_dict({**creds_data, "platform": platform.value})

    executor = CMSTaskExecutor.from_credentials(creds_map)
    client = CMSExecutorClient(agent_id="agent", agent_role=agent_role, executor=executor)
    tools = CMSExecutorTools(executor, AgentRole(agent_role))
    return executor, client, tools


# =============================================================================
# 与 MCP GEO 连接器集成
# =============================================================================

async def integrate_with_geo_pipeline(
    geo_insights: list[dict],
    executor: CMSTaskExecutor,
    agent_role: AgentRole = AgentRole.GEO_ANALYST,
) -> list[ExecutionResult]:
    """
    将 GEO 分析洞察直接转换为 CMS 执行任务
    
    这是 Gradial GEO 的核心能力：
    GEO Engine 输出洞察 → CMS Executor 自动写入
    
    Args:
        geo_insights: GEO Engine 输出的洞察列表
            [{"type": "seo_update", "platform": "wordpress", "resource_id": "posts/123", "data": {...}}, ...]
        executor: CMS 执行引擎
        agent_role: 执行 Agent 角色
    """
    client = CMSExecutorClient(agent_id="geo_pipeline", agent_role=agent_role, executor=executor)
    operations = []
    for insight in geo_insights:
        op = {
            "platform": insight["platform"],
            "operation": insight.get("operation", "update"),
            "resource_id": insight.get("resource_id", ""),
            "data": insight.get("data", {}),
            "resource_type": insight.get("resource_type", "post"),
            "preview_only": insight.get("preview_only", False),
        }
        operations.append(op)
    return await client.batch_execute(operations, parallel=True)
