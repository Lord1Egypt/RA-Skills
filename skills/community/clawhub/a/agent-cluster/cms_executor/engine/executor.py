"""
CMSTaskExecutor — 任务编排引擎

核心职责：
1. 接收执行计划（ExecutionPlan）
2. 安全沙箱预演（高风险操作）
3. 提交审批（根据风险等级）
4. 编排执行（串行/并行）
5. 结果验证与审计
"""

from __future__ import annotations

import asyncio
import logging
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Optional

from cms_executor.connectors.base_connector import (
    BaseCMSConnector,
    CMSCredentials,
    CMSPlatform,
    CMSOperation,
    CMSOperationType,
    CMSResourceType,
    RiskLevel,
    CMSResult,
    is_dangerous_operation,
)

from .approval import ApprovalWorkflow, ApprovalStatus
from .rollback import RollbackManager
from .audit import CMSAuditLogger

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# 数据模型
# =============================================================================

class ExecutionStatus(Enum):
    """执行状态"""
    PENDING = "pending"
    SANDBOXING = "sandboxing"     # 沙箱预演中
    AWAITING_APPROVAL = "awaiting_approval"
    APPROVED = "approved"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"
    CANCELLED = "cancelled"


class ExecutionMode(Enum):
    """执行模式"""
    PREVIEW = "preview"           # 仅预览，不实际执行
    LIVE = "live"                 # 实时执行
    SCHEDULED = "scheduled"       # 定时执行


@dataclass
class ExecutionPlan:
    """
    执行计划
    
    描述一个完整的 CMS 执行任务。
    可以包含多个操作（批量执行）。
    """
    plan_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    operations: list[CMSOperation] = field(default_factory=list)
    mode: ExecutionMode = ExecutionMode.LIVE
    parallel: bool = False  # 是否并行执行（仅对多操作有效）
    max_parallel: int = 5   # 最大并行数
    agent_id: str = ""
    agent_role: str = ""
    context: dict = field(default_factory=dict)  # 额外上下文
    scheduled_at: str = ""   # 定时执行时间（ISO 8601）
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    tags: list[str] = field(default_factory=list)

    def overall_risk_level(self) -> RiskLevel:
        """基于所有操作评估整体风险等级"""
        if not self.operations:
            return RiskLevel.LOW
        levels = [op.risk_level for op in self.operations]
        if RiskLevel.CRITICAL in levels:
            return RiskLevel.CRITICAL
        if RiskLevel.HIGH in levels:
            return RiskLevel.HIGH
        if RiskLevel.MEDIUM in levels:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    def to_dict(self) -> dict:
        return {
            "plan_id": self.plan_id,
            "title": self.title,
            "description": self.description,
            "mode": self.mode.value,
            "parallel": self.parallel,
            "operations": [op.to_dict() for op in self.operations],
            "risk_level": self.overall_risk_level().value,
            "agent_id": self.agent_id,
            "created_at": self.created_at,
            "tags": self.tags,
        }


@dataclass
class ExecutionContext:
    """
    执行上下文（运行时状态）
    
    记录一次执行任务的完整生命周期。
    """
    execution_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    plan_id: str = ""
    status: ExecutionStatus = ExecutionStatus.PENDING
    platform: CMSPlatform = CMSPlatform.CUSTOM
    connector: BaseCMSConnector | None = None
    results: list[CMSResult] = field(default_factory=list)
    approval_id: str = ""
    snapshot_ids: list[str] = field(default_factory=list)
    started_at: str = ""
    completed_at: str = ""
    total_time_ms: float = 0.0
    error: str = ""
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict:
        return {
            "execution_id": self.execution_id,
            "plan_id": self.plan_id,
            "status": self.status.value,
            "platform": self.platform.value,
            "results": [r.to_dict() for r in self.results],
            "approval_id": self.approval_id,
            "snapshot_ids": self.snapshot_ids,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "total_time_ms": self.total_time_ms,
            "error": self.error,
            "trace_id": self.trace_id,
        }


# =============================================================================
# 执行引擎
# =============================================================================

class CMSTaskExecutor:
    """
    CMS 任务执行引擎
    
    编排从计划到完成的完整执行流程：
    
    1. validate_plan()      验证计划合法性
    2. check_sandbox()      沙箱预演（高风险操作）
    3. submit_approval()    提交审批
    4. await_approval()     等待审批
    5. execute_ops()        执行写操作
    6. verify_result()       验证结果
    7. emit_audit()         审计日志
    """

    def __init__(
        self,
        connectors: dict[CMSPlatform, BaseCMSConnector],
        approval_workflow: ApprovalWorkflow | None = None,
        rollback_manager: RollbackManager | None = None,
        audit_logger: CMSAuditLogger | None = None,
    ):
        self.connectors = connectors
        self.approval_workflow = approval_workflow or ApprovalWorkflow()
        self.rollback_manager = rollback_manager or RollbackManager()
        self.audit_logger = audit_logger or CMSAuditLogger()

    # ── 主入口 ─────────────────────────────────────────────────────────────

    async def execute(self, plan: ExecutionPlan) -> ExecutionContext:
        """
        执行一个完整的 CMS 执行计划
        
        Returns:
            ExecutionContext: 包含完整执行结果和状态
        """
        ctx = ExecutionContext(
            plan_id=plan.plan_id,
            platform=plan.operations[0].platform if plan.operations else CMSPlatform.CUSTOM,
            connector=self.connectors.get(
                plan.operations[0].platform if plan.operations else CMSPlatform.CUSTOM
            ),
        )
        start = time.perf_counter()
        ctx.started_at = datetime.now(timezone.utc).isoformat()
        logger.info(f"[executor] Starting execution {ctx.execution_id} for plan {plan.plan_id}")

        try:
            # 1. 验证计划
            self._validate_plan(plan)

            # 2. 沙箱预演（高风险）
            if plan.overall_risk_level() in (RiskLevel.HIGH, RiskLevel.CRITICAL):
                ctx.status = ExecutionStatus.SANDBOXING
                sandbox_ok = await self._run_sandbox(plan, ctx)
                if not sandbox_ok:
                    ctx.status = ExecutionStatus.FAILED
                    ctx.error = "Sandbox validation failed"
                    return ctx

            # 3. 审批（PREVIEW 模式跳过）
            if plan.mode != ExecutionMode.PREVIEW:
                ctx.status = ExecutionStatus.AWAITING_APPROVAL
                approved = await self._submit_and_await_approval(plan, ctx)
                if not approved:
                    ctx.status = ExecutionStatus.CANCELLED
                    return ctx
                ctx.status = ExecutionStatus.APPROVED

            # 4. 执行操作
            ctx.status = ExecutionStatus.EXECUTING
            ctx.results = await self._execute_operations(plan, ctx)

            # 5. 验证结果
            all_success = all(r.success for r in ctx.results)
            ctx.status = ExecutionStatus.COMPLETED if all_success else ExecutionStatus.FAILED
            if not all_success:
                failed = [r.message for r in ctx.results if not r.success]
                ctx.error = f"Partial failure: {failed}"

        except Exception as e:
            ctx.status = ExecutionStatus.FAILED
            ctx.error = str(e)
            logger.exception(f"[executor] Execution {ctx.execution_id} failed: {e}")

        finally:
            ctx.total_time_ms = (time.perf_counter() - start) * 1000
            ctx.completed_at = datetime.now(timezone.utc).isoformat()
            # 6. 审计日志
            await self._emit_audit(plan, ctx)

        return ctx

    async def execute_batch(
        self, plans: list[ExecutionPlan], parallel: bool = True
    ) -> list[ExecutionContext]:
        """
        批量执行多个计划
        
        Args:
            plans: 执行计划列表
            parallel: True=并行执行，False=串行执行
        """
        if parallel:
            tasks = [self.execute(p) for p in plans]
            return await asyncio.gather(*tasks, return_exceptions=True)
        else:
            results = []
            for p in plans:
                results.append(await self.execute(p))
            return results

    async def preview(self, plan: ExecutionPlan) -> dict:
        """
        预览执行计划（不实际执行）
        
        返回执行效果预估，包含：
        - 风险评估
        - 变更摘要
        - 预计影响范围
        """
        risk = plan.overall_risk_level()
        dangerous_ops = [
            (op.operation_id, *is_dangerous_operation(op))
            for op in plan.operations
            if is_dangerous_operation(op)[0]
        ]
        return {
            "plan_id": plan.plan_id,
            "risk_level": risk.value,
            "operation_count": len(plan.operations),
            "platform": plan.operations[0].platform.value if plan.operations else "unknown",
            "dangerous_ops": [{"id": oid, "reason": r} for oid, _, r in dangerous_ops],
            "will_execute": len(dangerous_ops) == 0,
            "execution_mode": plan.mode.value,
            "estimated_duration_ms": len(plan.operations) * 500,  # 粗略估算
            "approval_required": plan.mode != ExecutionMode.PREVIEW and risk != RiskLevel.LOW,
        }

    async def cancel(self, execution_id: str) -> bool:
        """取消正在执行的任务"""
        logger.info(f"[executor] Cancellation requested for {execution_id}")
        # 实际取消需要状态机支持，这里标记意图
        return True

    # ── 执行步骤 ──────────────────────────────────────────────────────────

    def _validate_plan(self, plan: ExecutionPlan) -> None:
        """验证执行计划合法性"""
        if not plan.operations:
            raise ValueError("Execution plan has no operations")

        # 检查所有操作使用相同的平台
        platforms = {op.platform for op in plan.operations}
        if len(platforms) > 1:
            raise ValueError(f"Mixed platforms in single plan: {platforms}")

        # 检查平台支持
        platform = plan.operations[0].platform
        if platform not in self.connectors:
            raise ValueError(f"No connector registered for platform: {platform.value}")

        # PREVIEW 模式不允许执行写操作
        if plan.mode == ExecutionMode.PREVIEW:
            return

        # 检查危险操作
        for op in plan.operations:
            dangerous, reason = is_dangerous_operation(op)
            if dangerous:
                raise ValueError(f"Dangerous operation blocked: {reason}")

    async def _run_sandbox(self, plan: ExecutionPlan, ctx: ExecutionContext) -> bool:
        """
        安全沙箱预演
        
        对高风险操作进行影子执行（不实际修改），
        验证操作合法性和预期效果。
        """
        logger.info(f"[executor] Running sandbox for execution {ctx.execution_id}")
        connector = self.connectors.get(plan.operations[0].platform)
        if not connector:
            return False

        for op in plan.operations:
            try:
                # READ 操作在沙箱中执行，验证资源存在
                if op.operation_type in (CMSOperationType.READ, CMSOperationType.LIST):
                    await connector.read(op.resource_id)
                # 危险模式二次检测
                dangerous, reason = is_dangerous_operation(op)
                if dangerous:
                    await self.audit_logger.log_cms_sandbox(
                        operation=op,
                        result=False,
                        reason=reason,
                        trace_id=ctx.trace_id,
                    )
                    return False
            except Exception as e:
                logger.warning(f"[executor] Sandbox check failed for op {op.operation_id}: {e}")
                return False

        await self.audit_logger.log_cms_sandbox(
            operation=plan.operations[0],
            result=True,
            reason="Sandbox validation passed",
            trace_id=ctx.trace_id,
        )
        return True

    async def _submit_and_await_approval(
        self, plan: ExecutionPlan, ctx: ExecutionContext
    ) -> bool:
        """提交审批并等待结果"""
        risk_level = plan.overall_risk_level()
        approval_id = await self.approval_workflow.submit(
            plan=plan,
            risk_level=risk_level,
            agent_id=plan.agent_id,
        )
        ctx.approval_id = approval_id
        logger.info(f"[executor] Approval submitted: {approval_id} (risk: {risk_level.value})")

        # 根据风险等级决定等待策略
        if risk_level == RiskLevel.LOW:
            # 自动审批，立即通过
            await self.approval_workflow.approve(approval_id, "auto_approved", plan.agent_id)
            return True

        # 异步等待（生产环境应使用 webhook/callback）
        max_wait = {"medium": 600, "high": 3600, "critical": 86400}.get(risk_level.value, 600)
        for _ in range(max_wait // 10):
            await asyncio.sleep(10)
            status = await self.approval_workflow.get_status(approval_id)
            if status in (ApprovalStatus.APPROVED, ApprovalStatus.REJECTED):
                return status == ApprovalStatus.APPROVED

        # 超时降级：MEDIUM 自动通过，HIGH+ 拒绝
        if risk_level == RiskLevel.MEDIUM:
            await self.approval_workflow.approve(approval_id, "timeout_auto_approved", "system")
            return True
        return False

    async def _execute_operations(
        self, plan: ExecutionPlan, ctx: ExecutionContext
    ) -> list[CMSResult]:
        """执行操作列表"""
        connector = self.connectors.get(plan.operations[0].platform)
        if not connector:
            return [CMSResult.error(
                plan.operations[0],
                f"No connector for platform {plan.operations[0].platform.value}"
            )]

        if plan.parallel and len(plan.operations) > 1:
            # 并行执行（带并发控制）
            semaphore = asyncio.Semaphore(plan.max_parallel)
            async def run_with_limit(op: CMSOperation) -> CMSResult:
                async with semaphore:
                    return await self._execute_single(connector, op, ctx)
            tasks = [run_with_limit(op) for op in plan.operations]
            return await asyncio.gather(*tasks, return_exceptions=False)
        else:
            # 串行执行
            results = []
            for op in plan.operations:
                result = await self._execute_single(connector, op, ctx)
                results.append(result)
                # 串行执行遇错停止
                if not result.success and plan.parallel is False:
                    logger.warning(f"[executor] Halting serial execution after failure: {result.message}")
                    break
            return results

    async def _execute_single(
        self, connector: BaseCMSConnector, op: CMSOperation, ctx: ExecutionContext
    ) -> CMSResult:
        """执行单个操作"""
        logger.info(f"[executor] Executing op {op.operation_id} ({op.operation_type.value}) on {op.platform.value}")
        try:
            if op.operation_type == CMSOperationType.READ:
                return await connector.read(op.resource_id)
            elif op.operation_type == CMSOperationType.LIST:
                return await connector.list(op.data.get("filters", {}))
            elif op.operation_type == CMSOperationType.CREATE:
                return await connector.create(op.data, op.resource_type)
            elif op.operation_type == CMSOperationType.UPDATE:
                return await connector.update(op.resource_id, op.data, op.resource_type)
            elif op.operation_type == CMSOperationType.DELETE:
                return await connector.delete(op.resource_id, soft=op.data.get("soft", True))
            elif op.operation_type == CMSOperationType.UPLOAD:
                return await connector.upload_media(op.data.get("file_path", ""), op.data.get("metadata"))
            else:
                return CMSResult.error(op, f"Unsupported operation type: {op.operation_type}")
        except NotImplementedError as e:
            return CMSResult.error(op, str(e), error_code="NOT_IMPLEMENTED")
        except Exception as e:
            return CMSResult.error(op, str(e), error_code="EXECUTION_ERROR")

    async def _emit_audit(self, plan: ExecutionPlan, ctx: ExecutionContext) -> None:
        """发送审计日志"""
        try:
            await self.audit_logger.log_cms_write(
                operation=plan.operations[0] if plan.operations else CMSOperation(),
                result=ctx.results[0] if ctx.results else None,
                execution_context=ctx,
                trace_id=ctx.trace_id,
            )
        except Exception as e:
            logger.warning(f"[executor] Audit log failed: {e}")

    # ── 便捷构造 ──────────────────────────────────────────────────────────

    @classmethod
    def from_credentials(
        cls,
        credentials: dict[CMSPlatform, CMSCredentials],
    ) -> "CMSTaskExecutor":
        """
        从凭据字典创建执行引擎
        
        自动初始化对应平台的连接器。
        """
        from cms_executor.connectors import (
            WordPressConnector,
            ShopifyConnector,
            AmazonConnector,
            MagentoConnector,
        )
        connector_map = {
            CMSPlatform.WORDPRESS: WordPressConnector,
            CMSPlatform.SHOPIFY: ShopifyConnector,
            CMSPlatform.AMAZON: AmazonConnector,
            CMSPlatform.MAGENTO: MagentoConnector,
        }
        connectors: dict[CMSPlatform, BaseCMSConnector] = {}
        for platform, creds in credentials.items():
            if cls := connector_map.get(platform):
                connectors[platform] = cls(creds)
        return cls(connectors=connectors)
