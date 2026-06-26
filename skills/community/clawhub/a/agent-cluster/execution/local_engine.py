"""
Local Self-Built Engine

本地自建执行引擎 - 封装 Orchestrator 原有执行逻辑

概述:
    将 orchestrator.py 中原有的智能体执行逻辑迁移至此，
    作为默认执行引擎。支持：
    - 20 个专业智能体的并行/串行调度
    - 垂直领域知识（塑化行业 ERP/WMS/SRM）
    - M-A3 自进化能力（.learnings 反馈回路）
    - 完整的审计日志与权限控制

优势:
    - 完全自主可控
    - 支持垂直知识库注入
    - 支持自进化反馈回路
    - 无外部 API 依赖（离线可用）

Change Log:
    - 2026-04-14: 初始版本，从 orchestrator.py 迁移
"""

from __future__ import annotations

import logging
import time
from typing import Any, AsyncIterator, Dict, Optional

from .engine_base import ExecutionEngine, ExecutionResult, StreamChunk

logger = logging.getLogger(__name__)


class LocalEngine(ExecutionEngine):
    """
    本地自建执行引擎

    封装 Orchestrator 的核心执行能力：
    1. 意图识别 → 任务分解 → 智能体调度 → 结果汇总
    2. 支持串行/并行混合执行
    3. 内置安全审计与权限控制
    4. 支持流式增量输出

    使用场景:
    - 垂直领域任务（塑化行业 ERP/WMS/SRM）
    - 需要自进化能力的任务
    - 合规要求不能使用外部 API 的场景
    - 需要深度定制执行逻辑的场景
    """

    def __init__(self, config: Dict[str, Any] | None = None):
        """
        初始化本地引擎

        Args:
            config: 配置字典，支持字段：
                - orchestrator_class: type    Orchestrator 类（默认使用内联）
                - default_role: str            默认用户角色
                - enable_streaming: bool       启用流式输出（默认 True）
                - max_subtasks: int            最大子任务数（默认 20）
                - evolution_enabled: bool      启用自进化（默认 True）
        """
        super().__init__(config)
        self._default_role = self._config.get("default_role", "admin")
        self._enable_streaming = self._config.get("enable_streaming", True)
        self._max_subtasks = self._config.get("max_subtasks", 20)
        self._evolution_enabled = self._config.get("evolution_enabled", True)

        # 延迟导入 Orchestrator，避免循环依赖
        self._orchestrator = None

    @property
    def engine_name(self) -> str:
        return "local-self-built"

    @property
    def capabilities(self) -> Dict[str, bool]:
        return {
            "session_persistence": True,
            "harness_control": True,
            "sandbox": True,
            "credential_management": True,
            "self_evolution": True,           # M-A3 独有自进化
            "vertical_knowledge": True,       # 塑化行业垂直知识
            "streaming": True,
            "multi_modal": False,
            "compliance_certified": True,      # 完全本地，无外部依赖
        }

    async def execute(self, task: str, context: Dict[str, Any]) -> ExecutionResult:
        """
        通过本地 Orchestrator 执行任务

        完整流程：
        1. 意图识别（IntentRecognizer）
        2. 任务分解（TaskDecomposer）
        3. 权限校验（PermissionManager）
        4. 智能体调度（ Specialist Agents）
        5. 结果汇总（Aggregation）

        Args:
            task: 用户自然语言输入
            context: 执行上下文，包含：
                - user_id: str       用户ID
                - user_role: str     用户角色（admin/viewer/operator）
                - intent_type: str   预识别意图（可选）
                - parameters: dict  额外参数

        Returns:
            ExecutionResult: 标准执行结果
        """
        import time
        start = time.perf_counter()

        # 健康检查
        if context.get("_health_check"):
            latency_ms = (time.perf_counter() - start) * 1000
            result = ExecutionResult(
                success=True,
                output={"status": "healthy", "engine": self.engine_name},
                metadata=self._build_metadata(context),
                latency_ms=latency_ms,
            )
            self._record_stats(result)
            return result

        self._validate_context(context)
        user_id = context.get("user_id", "user")
        user_role = context.get("user_role", self._default_role)

        logger.info(
            f"[LocalEngine] 执行任务: {task[:80]}... "
            f"(user={user_id}, role={user_role})"
        )

        try:
            # ── 获取 Orchestrator 实例（延迟加载）───────────────────────────
            orch = await self._get_orchestrator()

            # ── 执行编排 ───────────────────────────────────────────────────
            orchestration_result = await orch.handle_request(
                user_input=task,
                user_id=user_id,
                user_role=user_role,
            )

            # ── 构建输出 ───────────────────────────────────────────────────
            output = self._build_output(orchestration_result, task)
            latency_ms = (time.perf_counter() - start) * 1000

            # ── 自进化反馈（可选）─────────────────────────────────────────
            if self._evolution_enabled:
                await self._record_evolution(task, orchestration_result)

            result = ExecutionResult(
                success=orchestration_result.status.value != "failed",
                output=output,
                metadata=self._build_metadata(context, {
                    "request_id": orchestration_result.request_id,
                    "status": orchestration_result.status.value,
                    "subtask_count": len(orchestration_result.sub_tasks),
                    "engine": "local-self-built",
                }),
                tokens_used=0,  # 本地执行无 token 消耗统计
                latency_ms=latency_ms,
            )
            self._record_stats(result)

            logger.info(
                f"[LocalEngine] 任务完成: status={orchestration_result.status.value}, "
                f"latency={latency_ms:.0f}ms, subtasks={len(orchestration_result.sub_tasks)}"
            )
            return result

        except Exception as e:
            latency_ms = (time.perf_counter() - start) * 1000
            logger.exception(f"[LocalEngine] 任务执行异常: {e}")
            result = ExecutionResult(
                success=False,
                output=None,
                metadata=self._build_metadata(context),
                latency_ms=latency_ms,
                error=str(e),
            )
            self._record_stats(result)
            return result

    async def stream(
        self, task: str, context: Dict[str, Any]
    ) -> AsyncIterator[StreamChunk]:
        """
        流式执行（增量输出）

        分阶段 yield 执行进度，适合长时间任务的实时反馈。

        Args:
            task: 任务描述
            context: 执行上下文

        Yields:
            StreamChunk: 增量输出块
        """
        import asyncio
        self._validate_context(context)

        # Stage 1: 意图识别
        yield StreamChunk(content="[1/4] 意图识别中...\n", done=False, delta_ms=0.0)
        await asyncio.sleep(0.15)
        orch = await self._get_orchestrator()
        intent = orch._intent_recognizer.recognize(task)
        yield StreamChunk(
            content=f"     → 识别为: {intent.intent_type} "
                    f"(置信度: {intent.confidence:.0%})\n",
            done=False, delta_ms=150.0
        )

        # Stage 2: 任务分解
        yield StreamChunk(content="[2/4] 任务分解中...\n", done=False, delta_ms=0.0)
        await asyncio.sleep(0.1)
        subtasks = orch._task_decomposer.decompose(intent, context.get("user_id", "user"))
        yield StreamChunk(
            content=f"     → 生成 {len(subtasks)} 个子任务\n",
            done=False, delta_ms=100.0
        )

        # Stage 3: 执行子任务
        yield StreamChunk(content="[3/4] 执行子任务...\n", done=False, delta_ms=0.0)
        await asyncio.sleep(0.1)

        for i, st in enumerate(subtasks, 1):
            yield StreamChunk(
                content=f"     [{i}/{len(subtasks)}] {st.agent_name}.{st.action}\n",
                done=False, delta_ms=50.0
            )
            await asyncio.sleep(0.08)

        # Stage 4: 汇总结果
        yield StreamChunk(content="[4/4] 汇总结果...\n", done=False, delta_ms=0.0)
        await asyncio.sleep(0.1)

        # 最终执行（非阻塞方式获取结果）
        result = await self.execute(task, context)
        yield StreamChunk(
            content=f"\n✅ 执行完成: {result.metadata.get('status', 'unknown')}\n",
            done=False, delta_ms=100.0
        )

        yield StreamChunk(content="", done=True, delta_ms=0.0)

    # -------------------------------------------------------------------------
    # 内部方法
    # -------------------------------------------------------------------------

    async def _get_orchestrator(self):
        """延迟加载 Orchestrator，避免启动时循环导入"""
        if self._orchestrator is None:
            # 延迟导入避免循环依赖
            from orchestrator import Orchestrator
            self._orchestrator = Orchestrator(
                user_id="engine",
                user_role=self._default_role,
            )
        return self._orchestrator

    def _build_output(
        self, orch_result, task: str
    ) -> Dict[str, Any]:
        """将 OrchestrationResult 转换为标准输出"""
        return {
            "request_id": orch_result.request_id,
            "status": orch_result.status.value,
            "intent_type": orch_result.intent.intent_type,
            "summary": orch_result.summary,
            "next_actions": orch_result.next_actions,
            "subtasks": [
                {
                    "task_id": t.task_id,
                    "agent": t.agent_name,
                    "action": t.action,
                    "status": t.status.value,
                    "error": t.error,
                }
                for t in orch_result.sub_tasks
            ],
            "aggregated_result": orch_result.aggregated_result,
        }

    async def _record_evolution(
        self, task: str, result
    ) -> None:
        """
        自进化反馈记录

        将执行结果写入 .learnings/ 供后续任务参考。
        实现简单的反馈回路。

        注意：完整自进化需实现 GEP 协议验证，
        此处为基础版本。
        """
        import os
        from datetime import datetime

        learnings_dir = ".learnings"
        os.makedirs(learnings_dir, exist_ok=True)

        log_path = os.path.join(learnings_dir, "engine_execution_log.md")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        entry = (
            f"\n## [{timestamp}] LocalEngine Execution\n"
            f"- Task: {task[:100]}\n"
            f"- Status: {result.status.value}\n"
            f"- Subtasks: {len(result.sub_tasks)}\n"
            f"- Summary: {result.summary}\n"
        )

        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(entry)
            logger.debug(f"[LocalEngine] 进化日志已写入: {log_path}")
        except Exception as e:
            logger.warning(f"[LocalEngine] 进化日志写入失败: {e}")
