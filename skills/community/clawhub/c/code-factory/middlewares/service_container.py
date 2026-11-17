"""
服务容器（ServiceContainer）—— 依赖注入容器。

管理所有中间件和步骤执行器的生命周期：
- CircuitBreaker：真单例，跨多次 run() 调用状态不丢失
- SideEffectTracker：每次 run() 新建
- TransactionManager：工厂方法，每次需要时新建
- 所有步骤执行器：延迟初始化

用法：
    container = ServiceContainer()
    breaker = container.get_circuit_breaker()
    guard = container.get_pipeline_guard()
    orchestrator = Orchestrator(request, container=container)
"""

from typing import Optional

from middlewares.circuit_breaker import CircuitBreaker, CircuitBreakerConfig
from middlewares.pipeline_guard import PipelineGuard
from middlewares.side_effect_log import SideEffectTracker
from middlewares.transaction_manager import TransactionManager
from middlewares.anti_corruption import AntiCorruptionLayer

from layers.preflight import PreflightRunner
from layers.spec_engine import SpecEngine
from layers.asset_generator import AssetGenerator
from layers.verifier import Verifier
from layers.retry_controller import RetryController
from layers.deliverer import Deliverer


class ServiceContainer:
    """依赖注入容器（v2.5 增强：生命周期管理 + Learner 集成）"""

    def __init__(self, breaker_config: Optional[CircuitBreakerConfig] = None):
        self._breaker_config = breaker_config

        # 中间件（延迟初始化）
        self._breaker: Optional[CircuitBreaker] = None
        self._acl: Optional[AntiCorruptionLayer] = None
        self._guard: Optional[PipelineGuard] = None

        # 步骤执行器（延迟初始化）
        self._preflight: Optional[PreflightRunner] = None
        self._spec_engine: Optional[SpecEngine] = None
        self._asset_generator: Optional[AssetGenerator] = None
        self._verifier: Optional[Verifier] = None
        self._retry_controller: Optional[RetryController] = None
        self._deliverer: Optional[Deliverer] = None

        # Learner（延迟初始化）
        self._learner = None
        self._learner_loaded = False

    # ── 中间件 ────────────────────────────────────

    def get_circuit_breaker(self) -> CircuitBreaker:
        """获取全局单例 CircuitBreaker"""
        if self._breaker is None:
            self._breaker = CircuitBreaker.get_instance(self._breaker_config)
        return self._breaker

    def get_anti_corruption_layer(self) -> AntiCorruptionLayer:
        """获取防腐层"""
        if self._acl is None:
            self._acl = AntiCorruptionLayer()
        return self._acl

    def get_pipeline_guard(self) -> PipelineGuard:
        """获取管道守护者"""
        if self._guard is None:
            self._guard = PipelineGuard(
                breaker=self.get_circuit_breaker(),
                acl=self.get_anti_corruption_layer(),
            )
        return self._guard

    # ── 工厂方法 ──────────────────────────────────

    def create_tracker(self) -> SideEffectTracker:
        """每次调用创建新的 SideEffectTracker"""
        return SideEffectTracker()

    def create_transaction_manager(self, target_dir) -> TransactionManager:
        """每次调用创建新的 TransactionManager"""
        from pathlib import Path
        return TransactionManager(Path(target_dir))

    # ── 步骤执行器 ────────────────────────────────

    def get_preflight(self) -> PreflightRunner:
        if self._preflight is None:
            self._preflight = PreflightRunner()
        return self._preflight

    def get_spec_engine(self) -> SpecEngine:
        if self._spec_engine is None:
            self._spec_engine = SpecEngine()
        return self._spec_engine

    def get_asset_generator(self) -> AssetGenerator:
        if self._asset_generator is None:
            self._asset_generator = AssetGenerator()
        return self._asset_generator

    def get_verifier(self) -> Verifier:
        if self._verifier is None:
            self._verifier = Verifier()
        return self._verifier

    def get_retry_controller(self) -> RetryController:
        if self._retry_controller is None:
            self._retry_controller = RetryController(max_retries=3)
        return self._retry_controller

    def get_deliverer(self) -> Deliverer:
        if self._deliverer is None:
            self._deliverer = Deliverer()
        return self._deliverer

    # ── Learner（延迟初始化） ─────────────────────

    def get_learner(self):
        """获取 Learner 实例"""
        if self._learner is None:
            from learnings.learner import Learner
            self._learner = Learner
        return self._learner

    def load_learnings(self, target_dir) -> None:
        """
        加载历史失败模式（从 Orchestrator 迁移到 ServiceContainer）。

        作为预检的一部分，在 Orchestrator.__init__ 中调用。
        """
        if self._learner_loaded:
            return
        try:
            from pathlib import Path
            from learnings.learner import Learner
            import logging

            learnings_path = Path(target_dir) / ".learnings"
            learner = Learner(learnings_path)
            report = learner.load()
            if report.should_skip_known_failures:
                logging.warning(
                    "Learner 检测到已知失败模式（%d 条），"
                    "建议检查环境配置或依赖版本",
                    report.total_patterns,
                )
        except Exception:
            pass
        finally:
            self._learner_loaded = True

    # ── 生命周期 ──────────────────────────────────

    def shutdown(self) -> None:
        """
        关闭容器，重置全局单例状态。

        主要用于测试：确保测试间 CircuitBreaker 状态不污染。
        """
        CircuitBreaker.reset_instance()
        self._breaker = None
        self._acl = None
        self._guard = None
        self._preflight = None
        self._spec_engine = None
        self._asset_generator = None
        self._verifier = None
        self._retry_controller = None
        self._deliverer = None
        self._learner = None
        self._learner_loaded = False
