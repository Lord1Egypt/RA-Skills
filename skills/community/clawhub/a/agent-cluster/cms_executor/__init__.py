"""
CMS Executor — Gradial GEO 直连执行系统

M-A3 Agent 集群的 CMS 直连执行能力。

核心模块:
- connectors/: 多平台 CMS 连接器（WordPress/Shopify/Amazon/Magento）
- engine/: 执行引擎（编排/审批/回滚/审计）
- agent_integration.py: Agent 调用接口 + MCP 协议暴露

快速开始:
    from agent_integration import create_executor_for_agent
    from connectors.base_connector import CMSPlatform

    executor, client, tools = create_executor_for_agent(
        credentials={
            CMSPlatform.WORDPRESS: {"api_base": "...", "api_key": "..."},
        },
        agent_role="content_creator",
    )

    result = await client.execute_wordpress(
        operation="update_seo",
        resource_id="posts/123",
        data={"seo_title": "...", "seo_description": "..."},
    )
"""

from .connectors import (
    BaseCMSConnector,
    CMSCredentials,
    CMSResource,
    CMSOperation,
    CMSPlatform,
    CMSResult,
    CMSResourceType,
    CMSOperationType,
    RiskLevel,
    CMSConnectionStatus,
    WordPressConnector,
    ShopifyConnector,
    AmazonConnector,
    MagentoConnector,
)

from .engine import (
    CMSTaskExecutor,
    ExecutionPlan,
    ExecutionStatus,
    ExecutionContext,
    ExecutionMode,
    ApprovalWorkflow,
    ApprovalStatus,
    ApprovalChain,
    RollbackManager,
    SnapshotStore,
    CMSAuditLogger,
)

from .agent_integration import (
    CMSExecutorClient,
    CMSExecutorTools,
    AgentRole,
    ROLE_PERMISSIONS,
    create_executor_for_agent,
    integrate_with_geo_pipeline,
    PermissionError,
)

__version__ = "1.0.0"
__all__ = [
    # Connectors
    "BaseCMSConnector",
    "CMSCredentials",
    "CMSResource",
    "CMSOperation",
    "CMSPlatform",
    "CMSResult",
    "CMSResourceType",
    "CMSOperationType",
    "RiskLevel",
    "CMSConnectionStatus",
    "WordPressConnector",
    "ShopifyConnector",
    "AmazonConnector",
    "MagentoConnector",
    # Engine
    "CMSTaskExecutor",
    "ExecutionPlan",
    "ExecutionStatus",
    "ExecutionContext",
    "ExecutionMode",
    "ApprovalWorkflow",
    "ApprovalStatus",
    "ApprovalChain",
    "RollbackManager",
    "SnapshotStore",
    "CMSAuditLogger",
    # Integration
    "CMSExecutorClient",
    "CMSExecutorTools",
    "AgentRole",
    "ROLE_PERMISSIONS",
    "create_executor_for_agent",
    "integrate_with_geo_pipeline",
    "PermissionError",
]
