"""
编排器（Orchestrator）—— 状态机驱动的步骤执行引擎。

职责：
1. 按 StepRegistry 定义的顺序执行 Phase 0 → Step 1-6
2. 管理每个步骤的状态转换（PENDING → RUNNING → SUCCESS/FAILED/ROLLED_BACK）
3. 协调 ServiceContainer、PipelineGuard、防腐层的交互
4. 任何步骤失败时触发 Saga 跨步骤补偿，不产生脏数据

v3.1 增强（延迟实例化 + 补偿注册表化 + Learner 时机修正）：
- Step3-6 使用 lambda 工厂闭包，在调用时读取最新 context（消除时序耦合）
- _make_compensation 完全基于 StepRegistry.has_side_effects 路由（消除硬编码）
- load_learnings() 移到 Phase 0 成功后（确保目标目录已存在）
"""

import logging
import shutil
import time
from pathlib import Path
from typing import Optional, Dict, Any

from contracts.input_schema import ProjectRequest
from contracts.output_schema import ProjectResult, StepResult, StepStatus
from contracts.step_context import StepContext
from contracts.exceptions import PreflightFailedError
from middlewares.circuit_breaker import (
    CircuitBreakerConfig,
    CircuitBreakerOpenError,
    GlobalTimeoutError,
)
from middlewares.side_effect_log import SideEffectTracker, SideEffectType
from middlewares.service_container import ServiceContainer
from middlewares.pipeline_guard import PipelineGuard
from middlewares.saga_coordinator import SagaCoordinator

from layers.step_registry import STEP_REGISTRY, get_step_definition
from layers.step_handlers.preflight_handler import PreflightHandler
from layers.step_handlers.snapshot_handler import SnapshotHandler
from layers.step_handlers.spec_handler import SpecHandler
from layers.step_handlers.asset_handler import AssetHandler
from layers.step_handlers.verify_handler import VerifyHandler
from layers.step_handlers.retry_handler import RetryHandler
from layers.step_handlers.delivery_handler import DeliveryHandler

logger = logging.getLogger(__name__)


class Orchestrator:
    """
    状态机驱动的编排引擎（v3.1 延迟实例化 + 补偿注册表化）。

    数据流：
        StepRegistry 定义步骤顺序 → Handler.execute() → PipelineGuard 执行 + 校验
          → commit_fn (来自注册表) → 写入 StepContext
          → 失败 → SagaCoordinator 补偿 has_side_effects 步骤
    """

    def __init__(
        self,
        request: ProjectRequest,
        target_dir: Optional[Path] = None,
        breaker_config: Optional[CircuitBreakerConfig] = None,
        container: Optional[ServiceContainer] = None,
    ):
        self.request = request
        self.target_dir = target_dir or Path("project_assets") / request.project_name
        self.container = container or ServiceContainer(breaker_config)

        self.breaker = self.container.get_circuit_breaker()
        self.guard: PipelineGuard = self.container.get_pipeline_guard()

        # 以下在 run() 中每次重建
        self.tracker: Optional[SideEffectTracker] = None
        self.saga: Optional[SagaCoordinator] = None

        self.context = StepContext(request=request)

    # ── 公共入口 ──────────────────────────────────

    def run(self) -> ProjectResult:
        """
        执行完整的交付流程（v3.1 延迟实例化 + 补偿注册表化 + Learner 时机修正）。

        增强：
        - Step3-6 使用 lambda 工厂，执行时才读取最新 context（消除时序耦合）
        - _make_compensation 完全基于 StepRegistry.has_side_effects 路由
        - load_learnings 在 Phase 0 通过后调用（确保目录已存在）
        """
        # 每次 run() 前重建可变状态，防止跨调用污染
        self.context.reset()
        self.saga = SagaCoordinator()
        self.tracker = self.container.create_tracker()
        self.breaker.reset_global_timer()

        result = ProjectResult(
            project_path=str(self.target_dir),
            project_name=self.request.project_name,
        )
        start_time = time.monotonic()
        self.breaker.start_global_timer()

        step_fn_map = self._build_step_fn_map()
        step_defs = STEP_REGISTRY
        phase0_idx = 0

        try:
            for idx, sd in enumerate(step_defs):
                step_name = sd.name
                step_fn = step_fn_map.get(step_name)

                if step_fn is None:
                    missing = StepResult(step_name=step_name, status=StepStatus.FAILED)
                    missing.mark_failed(f"步骤 '{step_name}' 未在 Orchestrator 中注册处理函数")
                    result.steps.append(missing)
                    result.status = StepStatus.FAILED
                    break

                # 防腐层输入校验 + 执行 + 输出校验
                if sd.depends_on:
                    prev_output = self.context.get_step_output(sd.depends_on)
                    step_result = self.guard.execute_with_validation(
                        step_name, step_fn, sd.depends_on, prev_output
                    )
                else:
                    step_result = self.guard.execute_step(step_name, step_fn)

                # Phase 0 失败 → 后续全部跳过
                if idx == phase0_idx and step_result.status == StepStatus.FAILED:
                    result.steps.append(step_result)
                    for remaining_sd in step_defs[1:]:
                        skip = StepResult(step_name=remaining_sd.name, status=StepStatus.SKIPPED)
                        skip.mark_skipped("Phase 0 环境预检未通过")
                        result.steps.append(skip)
                    result.status = StepStatus.FAILED
                    break

                # v3.1: Phase 0 通过后加载学习器（此时目标目录已确保可写）
                if idx == phase0_idx and step_result.ok:
                    self.container.load_learnings(self.target_dir)

                # 步骤成功 → 通过注册表的 commit_fn 统一写入 StepContext
                if step_result.ok and step_result.output_data:
                    self._commit_step_output(sd.name, step_result.output_data)

                # Saga 补偿注册：基于 StepRegistry.has_side_effects（v3.1：完全注册表驱动）
                if step_result.ok and sd.has_side_effects:
                    compensation = self._make_compensation(sd.name)
                    if compensation:
                        self.saga.register(sd.name, compensation)

                result.steps.append(step_result)

                # 步骤失败 → 执行 Saga 补偿所有已完成步骤
                if step_result.status == StepStatus.FAILED:
                    result.status = StepStatus.FAILED
                    if self.saga.registered_steps:
                        logger.warning(
                            "步骤 '%s' 失败，触发 Saga 补偿 %d 个已完成步骤",
                            step_name, len(self.saga.registered_steps),
                        )
                        compensated = self.saga.compensate_all()
                        for existing_step in result.steps:
                            if existing_step.step_name in compensated:
                                existing_step.status = StepStatus.ROLLED_BACK
                                existing_step.warnings.append("Saga 补偿：已回滚")
                    break

        except (CircuitBreakerOpenError, GlobalTimeoutError) as e:
            result.status = StepStatus.FAILED
            result.steps.append(StepResult(
                step_name="全局",
                status=StepStatus.FAILED,
                errors=[f"全局保护触发: {e}"],
            ))
        except Exception as e:
            result.status = StepStatus.FAILED
            logger.exception("Orchestrator.run() 未捕获异常: %s", e)
            try:
                if self.saga:
                    self.saga.compensate_all()
            except Exception:
                logger.exception("Saga 补偿过程中发生异常")
            result.steps.append(StepResult(
                step_name="全局",
                status=StepStatus.FAILED,
                errors=[f"未预期异常: {type(e).__name__}: {e}"],
            ))

        # 完成结果组装
        if result.all_passed:
            result.status = StepStatus.SUCCESS
        result.generated_files = self.context.generated_assets
        result.total_duration_seconds = time.monotonic() - start_time

        self.tracker.record(
            SideEffectType.FILE_CREATE,
            str(self.target_dir),
            after_state=str(result.generated_files),
        )
        return result

    # ── 步骤函数映射（v3.1：延迟实例化，消除时序耦合） ──

    def _build_step_fn_map(self) -> Dict[str, Any]:
        """
        构建步骤名→可调用函数的映射。

        v3.2 增强：
        - Phase0/Step1/Step2：无运行时依赖，直接实例化
        - Step3-6：使用 lambda 工厂闭包，执行时才读取最新 context 数据
        - tracker 通过闭包快照捕获（trk = self.tracker），防止后续代码修改 self.tracker
        """
        trk = self.tracker  # 闭包快照，防止引用被后续代码覆盖

        return {
            # 无运行时依赖：直接实例化
            "Phase0": PreflightHandler(
                target_dir=self.target_dir,
                required_python=self.request.target_python_version,
                required_deps=self.request.dependencies,
            ).execute,
            "Step1": SnapshotHandler(
                python_version=self.request.target_python_version,
                dependencies=self.request.dependencies,
                target_directory=str(self.target_dir),
                acl=self.guard.acl,
            ).execute,
            "Step2": SpecHandler(
                description=self.request.description,
                project_type=self.request.project_type,
                acceptance_criteria=self.request.acceptance_criteria,
                acl=self.guard.acl,
            ).execute,

            # 有运行时依赖：lambda 工厂 → 执行时才读取最新 context
            "Step3": lambda trk=trk: AssetHandler(
                project_name=self.request.project_name,
                derived_spec=self.context.derived_spec,
                target_dir=self.target_dir,
                container=self.container,
                tracker=trk,
            ).execute(),
            "Step4": lambda: VerifyHandler(
                target_dir=self.target_dir,
                assets=self.context.generated_assets,
                acl=self.guard.acl,
            ).execute(),
            "Step5": lambda trk=trk: RetryHandler(
                context=self.context,
                verifier=self.container.get_verifier(),
                asset_generator=self.container.get_asset_generator(),
                target_dir=self.target_dir,
                tracker=trk,
                guard=self.guard,
            ).execute(),
            "Step6": lambda: DeliveryHandler(
                project_path=self.target_dir,
                project_name=self.request.project_name,
                context=self.context,
            ).execute(),
        }

    # ── 统一写入入口（注册表驱动） ─────────────────

    def _commit_step_output(self, step_name: str, output: Dict[str, Any]) -> None:
        """通过 StepRegistry 的 commit_fn 回调统一写入 StepContext。"""
        sd = get_step_definition(step_name)
        if sd and sd.commit_fn:
            sd.commit_fn(self.context, output)

    # ── Saga 补偿（v3.1：完全注册表驱动，消除硬编码） ──

    def _make_compensation(self, step_name: str):
        """
        创建步骤的 Saga 补偿函数。

        v3.1：完全基于 StepRegistry.has_side_effects 路由。
        不再硬编码 if step_name == "Step3"——任何标记 has_side_effects 的步骤
        都能获得补偿，补偿逻辑由步骤名路由到对应的实现。
        """
        compensations = {
            "Step3": self._make_asset_compensation,
            "Step5": self._make_retry_compensation,
        }
        factory = compensations.get(step_name)
        if factory:
            return factory()
        return None

    def _make_file_cleanup_compensation(self, cleanup_subdirs: bool = True):
        """
        创建通用文件清理补偿函数（v3.2：消除 _make_asset/_make_retry 代码重复）。

        基于 SideEffectTracker 记录的 created_files 精准清理，
        避免宽泛 glob 模式误删用户文件。

        Args:
            cleanup_subdirs: 是否清理 src/tests/docs 子目录（Step3 需要，Step5 不需要）
        """
        tracker = self.tracker
        target_dir = self.target_dir

        def _compensate() -> None:
            if not target_dir.exists():
                return
            created = tracker.get_created_files()
            for rel_path in created:
                file_path = target_dir / rel_path
                try:
                    if file_path.is_file():
                        file_path.unlink()
                    elif file_path.is_dir():
                        shutil.rmtree(file_path, ignore_errors=True)
                except OSError:
                    pass
            if cleanup_subdirs:
                for subdir in ("src", "tests", "docs"):
                    p = target_dir / subdir
                    if p.exists():
                        try:
                            shutil.rmtree(p, ignore_errors=True)
                        except OSError:
                            pass

        return _compensate

    def _make_asset_compensation(self):
        """Step3 补偿：精准删除 tracker 记录的文件 + 清理子目录"""
        return self._make_file_cleanup_compensation(cleanup_subdirs=True)

    def _make_retry_compensation(self):
        """Step5 补偿：精准删除重试产生的 tracker 记录文件"""
        return self._make_file_cleanup_compensation(cleanup_subdirs=False)
