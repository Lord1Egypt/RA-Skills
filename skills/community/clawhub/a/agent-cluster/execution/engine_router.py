"""
Execution Engine Router

执行引擎路由器 - 根据任务特征智能选择最优引擎

功能:
    1. 维护多个引擎实例
    2. 支持路由规则配置（YAML）
    3. 基于任务类型/场景/复杂度选择引擎
    4. 支持引擎降级（主引擎失败 → 备用引擎）
    5. 完整路由日志（引擎切换可追踪）

路由策略:
    优先级从高到低：
    1. 显式指定（context.engine_hint）
    2. 场景规则匹配（scene_rules）
    3. 意图类型规则（intent_rules）
    4. 关键词匹配（keyword_rules）
    5. 默认引擎（default_engine）

Change Log:
    - 2026-04-14: 初始版本
"""

from __future__ import annotations

import logging
import re
import time as _time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set

from .engine_base import (
    AuthProfile,
    AuthProfileError,
    ExecutionEngine,
    ExecutionResult,
)
from .circuit_breaker import (
    CircuitOpenError,
    CircuitState,
    GlobalCircuitBreaker,
    ModelHealthRegistry,
    check_model_health,
    generate_health_report,
    report_request_result,
)

logger = logging.getLogger(__name__)


# =============================================================================
# 路由上下文
# =============================================================================


class RoutingStrategy(Enum):
    """路由策略"""
    EXPLICIT = "explicit"       # 显式指定（优先级最高）
    SCENE_MATCH = "scene"      # 场景匹配
    INTENT_MATCH = "intent"    # 意图类型匹配
    KEYWORD_MATCH = "keyword"  # 关键词匹配
    DEFAULT = "default"        # 默认引擎


@dataclass
class RoutingContext:
    """
    路由决策上下文

    在调用 route() 前构建，包含任务的所有特征
    """
    task: str                    # 原始任务描述
    intent_type: str             # 意图类型（stock_query/purchase/logistics/...）
    user_role: str               # 用户角色
    scene: str                   # 场景标签（compliance/dev/general/...）
    entities: Dict[str, Any]     # 提取的实体
    engine_hint: Optional[str] = None  # 显式指定的引擎（优先级最高）
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.task_lower = self.task.lower()

    def has_keywords(self, keywords: List[str]) -> bool:
        """检查任务是否包含指定关键词"""
        return any(kw.lower() in self.task_lower for kw in keywords)


@dataclass
class RoutingDecision:
    """
    路由决策结果

    记录选择过程和最终决策
    """
    engine: ExecutionEngine
    strategy: RoutingStrategy
    reason: str
    confidence: float            # 置信度 0.0-1.0
    fallback_engines: List[ExecutionEngine]  # 备用引擎列表

    def to_dict(self) -> Dict[str, Any]:
        return {
            "engine": self.engine.engine_name,
            "strategy": self.strategy.value,
            "reason": self.reason,
            "confidence": self.confidence,
            "fallback_count": len(self.fallback_engines),
        }


@dataclass
class RoutingRule:
    """
    路由规则

    支持精确匹配、正则匹配、权重配置
    """
    name: str                     # 规则名称（唯一标识）
    engine: str                   # 目标引擎名称
    priority: int = 100           # 优先级（越小越先匹配）
    intent_types: List[str] = field(default_factory=list)   # 意图类型列表
    scenes: List[str] = field(default_factory=list)       # 场景标签
    keywords: List[str] = field(default_factory=list)       # 关键词列表
    keyword_patterns: List[str] = field(default_factory=list)  # 正则模式
    user_roles: List[str] = field(default_factory=list)    # 限制的用户角色
    confidence_boost: float = 0.0  # 匹配时置信度加成

    def matches(self, ctx: RoutingContext) -> bool:
        """检查规则是否匹配给定上下文"""
        # 意图类型过滤
        if self.intent_types and ctx.intent_type not in self.intent_types:
            return False

        # 场景过滤
        if self.scenes and ctx.scene not in self.scenes:
            return False

        # 用户角色过滤
        if self.user_roles and ctx.user_role not in self.user_roles:
            return False

        # 关键词匹配
        if self.keywords:
            if not ctx.has_keywords(self.keywords):
                return False

        # 正则模式匹配
        if self.keyword_patterns:
            matched = any(
                re.search(pattern, ctx.task, re.IGNORECASE)
                for pattern in self.keyword_patterns
            )
            if not matched:
                return False

        return True


# =============================================================================
# 引擎路由器
# =============================================================================


class EngineRouter:
    """
    执行引擎路由器

    核心功能:
    1. 管理多个引擎实例（注册/注销）
    2. 根据任务上下文选择最优引擎
    3. 支持路由规则热更新（从 YAML 重新加载）
    4. 引擎降级：当主引擎失败时自动切换备用引擎
    5. 路由统计与监控

    使用示例:
        router = EngineRouter()

        # 注册引擎
        router.register_engine(LocalEngine())
        router.register_engine(ClaudeMAEngine())
        router.register_engine(DeepSeekEngine())

        # 加载规则
        router.load_rules_from_yaml("config/engines.yaml")

        # 路由决策
        decision = router.route(RoutingContext(
            task="查询库存情况",
            intent_type="stock_query",
            user_role="viewer",
            scene="general",
            entities={},
        ))

        # 执行
        result = await decision.engine.execute(task, context)
    """

    def __init__(
        self,
        circuit_breaker_enabled: bool = True,
        health_registry_path: str = "model_health.json",
    ):
        self._engines: Dict[str, ExecutionEngine] = {}
        self._rules: List[RoutingRule] = []
        self._default_engine: Optional[str] = None

        # ── Phase 2: 全局熔断器 & 健康注册中心 ───────────────────────────
        self._circuit_breaker_enabled = circuit_breaker_enabled
        self._health_registry_path = health_registry_path
        # 全局单例（延迟初始化）
        self._cb_instance: Optional[GlobalCircuitBreaker] = None
        self._registry_instance: Optional[ModelHealthRegistry] = None

        # 注册全局健康注册表（让 report_request_result 共享同一实例）
        if self._circuit_breaker_enabled:
            from .circuit_breaker import set_global_registry
            self._registry_instance = ModelHealthRegistry(
                persist_path=self._health_registry_path
            )
            set_global_registry(self._registry_instance)

        self._stats = {
            "total_routes": 0,
            "strategy_counts": {s.value: 0 for s in RoutingStrategy},
            "engine_usage": {},   # engine_name → count
            "circuit_rejections": 0,   # 熔断器拒绝次数
        }
        logger.info(
            f"[EngineRouter] 初始化完成 | circuit_breaker={circuit_breaker_enabled} | "
            f"health_registry={health_registry_path}"
        )

    # -------------------------------------------------------------------------
    # 引擎管理
    # -------------------------------------------------------------------------

    def register_engine(
        self,
        engine: ExecutionEngine,
        set_default: bool = False,
    ) -> None:
        """
        注册执行引擎

        Args:
            engine: 引擎实例
            set_default: 是否设为默认引擎
        """
        name = engine.engine_name
        if name in self._engines:
            logger.warning(
                f"[EngineRouter] 引擎 {name} 已存在，将被替换"
            )
        self._engines[name] = engine
        if set_default or not self._default_engine:
            self._default_engine = name

        logger.info(
            f"[EngineRouter] 注册引擎: {name}, "
            f"capabilities={engine.capabilities}, "
            f"default={set_default or name == self._default_engine}"
        )

    def unregister_engine(self, name: str) -> bool:
        """
        注销引擎

        Returns:
            bool: 是否成功注销
        """
        if name not in self._engines:
            logger.warning(f"[EngineRouter] 尝试注销未知引擎: {name}")
            return False

        del self._engines[name]
        if self._default_engine == name:
            self._default_engine = next(iter(self._engines), None)

        logger.info(f"[EngineRouter] 注销引擎: {name}")
        return True

    def get_engine(self, name: str) -> Optional[ExecutionEngine]:
        """根据名称获取引擎"""
        return self._engines.get(name)

    def list_engines(self) -> List[Dict[str, Any]]:
        """列出所有已注册引擎及其状态"""
        return [
            {
                "name": name,
                "capabilities": eng.capabilities,
                "is_default": name == self._default_engine,
                "stats": eng.get_stats(),
            }
            for name, eng in self._engines.items()
        ]

    # -------------------------------------------------------------------------
    # Phase 2: 全局熔断器 & 健康注册中心
    # -------------------------------------------------------------------------

    @property
    def circuit_breaker(self) -> GlobalCircuitBreaker:
        """获取全局断路器（延迟初始化单例）"""
        if self._cb_instance is None:
            self._cb_instance = GlobalCircuitBreaker.get_instance()
        return self._cb_instance

    @property
    def health_registry(self) -> ModelHealthRegistry:
        """获取模型健康注册表（延迟初始化）"""
        if self._registry_instance is None:
            self._registry_instance = ModelHealthRegistry(
                persist_path=self._health_registry_path
            )
        return self._registry_instance

    def check_engine_available(self, engine: ExecutionEngine) -> tuple[bool, str]:
        """
        检查引擎对应的模型是否可用

        Args:
            engine: 目标引擎

        Returns:
            (can_proceed, reason): 是否可请求 + 原因
        """
        if not self._circuit_breaker_enabled:
            return True, "disabled"

        # 引擎 → 模型名映射
        model = self._resolve_engine_model(engine)
        return check_model_health(model)

    def _resolve_engine_model(self, engine: ExecutionEngine) -> str:
        """
        从引擎实例解析模型标识符

        策略（按优先级）:
            1. engine.model 属性（DeepSeekEngine 等有 .model）
            2. engine.engine_name（作为降级）
            3. engine.engine_name 本身
        """
        # 直接属性查找
        model = getattr(engine, "_model", None)
        if model:
            return model

        # engine_name 降级
        name = engine.engine_name
        if name.startswith("domestic-"):
            return name.replace("domestic-", "deepseek-")
        if name.startswith("claude-"):
            return name
        return name

    def _report_engine_result(
        self,
        engine: ExecutionEngine,
        success: bool,
        latency_ms: float,
        error: Optional[str] = None,
        is_probe: bool = False,
    ) -> Dict[str, Any]:
        """
        报告引擎执行结果到全局熔断器和健康注册表

        Args:
            engine:     目标引擎
            success:    是否成功
            latency_ms: 延迟（毫秒）
            error:      错误信息（失败时）
            is_probe:   是否为探测请求

        Returns:
            Dict: report_request_result 返回值
        """
        if not self._circuit_breaker_enabled:
            return {}

        model = self._resolve_engine_model(engine)
        return report_request_result(
            model=model,
            success=success,
            error=error,
            is_probe=is_probe,
        )

    # -------------------------------------------------------------------------
    # 规则管理
    # -------------------------------------------------------------------------

    def add_rule(self, rule: RoutingRule) -> None:
        """添加路由规则"""
        self._rules.append(rule)
        # 按优先级排序
        self._rules.sort(key=lambda r: r.priority)
        logger.info(f"[EngineRouter] 添加路由规则: {rule.name} → {rule.engine}")

    def load_rules_from_yaml(self, yaml_path: str) -> int:
        """
        从 YAML 文件加载路由规则

        Args:
            yaml_path: YAML 文件路径

        Returns:
            int: 加载的规则数量
        """
        import yaml
        try:
            with open(yaml_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"[EngineRouter] 规则文件不存在: {yaml_path}")
            return 0
        except Exception as e:
            logger.error(f"[EngineRouter] 加载规则失败: {e}")
            return 0

        routing_config = config.get("routing", {})
        rules_config = routing_config.get("rules", [])

        count = 0
        for rule_dict in rules_config:
            try:
                rule = RoutingRule(
                    name=rule_dict["name"],
                    engine=rule_dict["engine"],
                    priority=rule_dict.get("priority", 100),
                    intent_types=rule_dict.get("intent_types", []),
                    scenes=rule_dict.get("scenes", []),
                    keywords=rule_dict.get("keywords", []),
                    keyword_patterns=rule_dict.get("keyword_patterns", []),
                    user_roles=rule_dict.get("user_roles", []),
                    confidence_boost=rule_dict.get("confidence_boost", 0.0),
                )
                self.add_rule(rule)
                count += 1
            except (KeyError, TypeError) as e:
                logger.warning(f"[EngineRouter] 规则解析失败: {rule_dict}, error: {e}")

        # 设置默认引擎
        default = routing_config.get("default_engine")
        if default and default in self._engines:
            self._default_engine = default
            logger.info(f"[EngineRouter] 设置默认引擎: {default}")

        logger.info(f"[EngineRouter] 从 {yaml_path} 加载了 {count} 条路由规则")
        return count

    def add_default_rules(self) -> None:
        """
        添加默认路由规则

        当没有 YAML 配置文件时使用，覆盖常见场景
        """
        default_rules = [
            # 合规场景 → 国产模型
            RoutingRule(
                name="compliance_scene",
                engine="domestic-deepseek-chat",
                priority=10,
                scenes=["compliance"],
                confidence_boost=0.5,
            ),
            # 通用开发任务 → Claude MA
            RoutingRule(
                name="general_dev",
                engine="claude-managed-agents",
                priority=30,
                intent_types=["general", "code", "analysis"],
                keywords=["写代码", "调试", "分析", "代码", "debug", "analyze"],
                confidence_boost=0.2,
            ),
            # 库存/采购/物流 → Local（垂直知识）
            RoutingRule(
                name="vertical_industry",
                engine="local-self-built",
                priority=20,
                intent_types=[
                    "stock_query", "purchase", "logistics",
                    "finance", "replenishment", "document",
                ],
                confidence_boost=0.3,
            ),
            # 离线/内网环境 → Local
            RoutingRule(
                name="offline_mode",
                engine="local-self-built",
                priority=15,
                scenes=["offline", "dev"],
                confidence_boost=0.4,
            ),
            # 关键词：合规/信创/国产 → 国产模型
            RoutingRule(
                name="domestic_keywords",
                engine="domestic-deepseek-chat",
                priority=25,
                keyword_patterns=[
                    r"合规", r"信创", r"国产", r"等保",
                    r"domestic", r"compliance", r"domesticated",
                ],
                confidence_boost=0.2,
            ),
        ]

        for rule in default_rules:
            # 检查目标引擎是否存在
            if rule.engine in self._engines:
                self.add_rule(rule)
            else:
                # 尝试模糊匹配
                matched = [
                    name for name in self._engines
                    if rule.engine.split("-")[-1] in name
                ]
                if matched:
                    rule.engine = matched[0]
                    self.add_rule(rule)

    # -------------------------------------------------------------------------
    # 核心路由逻辑
    # -------------------------------------------------------------------------

    def route(self, ctx: RoutingContext) -> RoutingDecision:
        """
        根据任务上下文选择最优引擎

        路由策略优先级:
            1. 显式指定（engine_hint）
            2. 场景规则
            3. 意图类型规则
            4. 关键词匹配
            5. 默认引擎

        Args:
            ctx: 路由上下文

        Returns:
            RoutingDecision: 路由决策
        """
        self._stats["total_routes"] += 1

        # ── 策略 1: 显式指定 ──────────────────────────────────────────────
        if ctx.engine_hint:
            engine = self._engines.get(ctx.engine_hint)
            if engine:
                decision = RoutingDecision(
                    engine=engine,
                    strategy=RoutingStrategy.EXPLICIT,
                    reason=f"显式指定: {ctx.engine_hint}",
                    confidence=1.0,
                    fallback_engines=self._get_fallback_engines(ctx, exclude=engine.engine_name),
                )
                self._record_route(decision)
                return decision
            else:
                logger.warning(
                    f"[EngineRouter] 显式指定的引擎不存在: {ctx.engine_hint}, "
                    f"将尝试自动路由"
                )

        # ── 策略 2-4: 规则匹配 ─────────────────────────────────────────────
        best_rule: Optional[RoutingRule] = None
        best_confidence = 0.0
        matched_strategy = RoutingStrategy.DEFAULT

        for rule in self._rules:
            if rule.matches(ctx):
                confidence = 0.5 + rule.confidence_boost
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_rule = rule
                    # 确定匹配策略
                    if rule.scenes:
                        matched_strategy = RoutingStrategy.SCENE_MATCH
                    elif rule.intent_types:
                        matched_strategy = RoutingStrategy.INTENT_MATCH
                    elif rule.keywords or rule.keyword_patterns:
                        matched_strategy = RoutingStrategy.KEYWORD_MATCH

        if best_rule and best_rule.engine in self._engines:
            engine = self._engines[best_rule.engine]
            reason = (
                f"规则[{best_rule.name}]匹配: "
                f"intent={ctx.intent_type}, scene={ctx.scene}, "
                f"confidence={best_confidence:.2f}"
            )
            decision = RoutingDecision(
                engine=engine,
                strategy=matched_strategy,
                reason=reason,
                confidence=min(best_confidence, 1.0),
                fallback_engines=self._get_fallback_engines(ctx, exclude=engine.engine_name),
            )
            self._record_route(decision)
            return decision

        # ── 策略 5: 默认引擎 ───────────────────────────────────────────────
        if self._default_engine and self._default_engine in self._engines:
            engine = self._engines[self._default_engine]
            decision = RoutingDecision(
                engine=engine,
                strategy=RoutingStrategy.DEFAULT,
                reason=f"使用默认引擎: {self._default_engine}",
                confidence=0.3,
                fallback_engines=self._get_fallback_engines(
                    ctx, exclude=engine.engine_name
                ),
            )
            self._record_route(decision)
            return decision

        # ── 兜底: 任意可用引擎 ─────────────────────────────────────────────
        if self._engines:
            engine = next(iter(self._engines.values()))
            decision = RoutingDecision(
                engine=engine,
                strategy=RoutingStrategy.DEFAULT,
                reason="兜底: 任意可用引擎",
                confidence=0.1,
                fallback_engines=[],
            )
            self._record_route(decision)
            return decision

        # 完全无引擎
        raise RuntimeError(
            "[EngineRouter] 没有可用的执行引擎，请先注册至少一个引擎"
        )

    def route_and_execute(
        self, task: str, context: Dict[str, Any]
    ) -> ExecutionResult:
        """
        路由并执行（同步封装）

        内部自动处理降级逻辑。

        Args:
            task: 任务描述
            context: 执行上下文

        Returns:
            ExecutionResult: 执行结果
        """
        import asyncio

        async def _execute():
            return await self.route_and_execute_async(task, context)

        return asyncio.run(_execute())

    async def route_and_execute_async(
        self, task: str, context: Dict[str, Any]
    ) -> ExecutionResult:
        """
        路由并执行（异步，支持流式降级）

        Phase 2 集成:
            - 路由前：GlobalCircuitBreaker 健康检查（过滤熔断中的引擎）
            - 执行后：report_request_result 更新健康度

        Args:
            task: 任务描述
            context: 执行上下文

        Returns:
            ExecutionResult: 执行结果
        """
        # 构建路由上下文
        ctx = RoutingContext(
            task=task,
            intent_type=context.get("intent_type", "mixed"),
            user_role=context.get("user_role", "viewer"),
            scene=context.get("scene", "general"),
            entities=context.get("entities", {}),
            engine_hint=context.get("engine_hint"),
            metadata=context,
        )

        decision = self.route(ctx)

        # ── Phase 2: 熔断器预检查 ─────────────────────────────────────────
        if self._circuit_breaker_enabled:
            can_run, reason = self.check_engine_available(decision.engine)
            if not can_run:
                model = self._resolve_engine_model(decision.engine)
                snap = self.circuit_breaker.get_snapshot(model)
                remaining = snap.remaining_open_time
                self._stats["circuit_rejections"] += 1
                logger.warning(
                    f"[EngineRouter] 熔断器阻止引擎 {decision.engine.engine_name}: "
                    f"reason={reason}, remaining={remaining:.1f}s"
                )
                # 尝试备用引擎
                for fallback in decision.fallback_engines:
                    fb_can, fb_reason = self.check_engine_available(fallback)
                    if fb_can:
                        logger.info(
                            f"[EngineRouter] 切换到备用引擎 {fallback.engine_name} "
                            f"(主引擎熔断中: {reason})"
                        )
                        decision = RoutingDecision(
                            engine=fallback,
                            strategy=decision.strategy,
                            reason=f"[熔断切换] {decision.reason} | {fb_reason}",
                            confidence=decision.confidence * 0.8,
                            fallback_engines=[
                                f for f in decision.fallback_engines
                                if f.engine_name != fallback.engine_name
                            ],
                        )
                        decision.engine = fallback
                        can_run = True
                        break

                if not can_run:
                    # 所有引擎均不可用，返回熔断拒绝结果
                    snap = self.circuit_breaker.get_snapshot(
                        self._resolve_engine_model(decision.engine)
                    )
                    result = ExecutionResult(
                        success=False,
                        output=None,
                        metadata={
                            "_circuit_open": True,
                            "_circuit_model": self._resolve_engine_model(decision.engine),
                            "_remaining_open_time": round(snap.remaining_open_time, 2),
                        },
                        latency_ms=0.0,
                        error=(
                            f"[CircuitBreaker OPEN] 所有引擎均不可用，"
                            f"model={self._resolve_engine_model(decision.engine)}, "
                            f"retry in {snap.remaining_open_time:.1f}s"
                        ),
                    )
                    return result

        logger.info(
            f"[EngineRouter] 路由决策: engine={decision.engine.engine_name}, "
            f"strategy={decision.strategy.value}, "
            f"confidence={decision.confidence:.2f}"
        )

        start_ts = _time.monotonic()

        # 执行主引擎
        result = await decision.engine.execute(task, context)

        # ── Phase 2: 执行后健康度上报 ───────────────────────────────────
        latency_ms = result.latency_ms or max(0.0, (_time.monotonic() - start_ts) * 1000)
        self._report_engine_result(
            engine=decision.engine,
            success=result.success,
            latency_ms=latency_ms,
            error=result.error,
            is_probe=context.get("_is_probe", False),
        )

        # ── 引擎级降级：主引擎失败时尝试备用引擎 ───────────────────────────
        if not result.success and decision.fallback_engines:
            # 记录主引擎 Key 失败（若支持 AuthProfile）
            primary_key_id = self._extract_key_id_from_result(result, decision.engine)
            if primary_key_id:
                self._report_engine_key_failure(decision.engine, primary_key_id, result.error)

            logger.warning(
                f"[EngineRouter] 主引擎 {decision.engine.engine_name} 执行失败，"
                f"尝试降级 ({len(decision.fallback_engines)} 个备用引擎)"
            )
            for fallback in decision.fallback_engines:
                logger.info(f"[EngineRouter] 尝试备用引擎: {fallback.engine_name}")

                # ── 备用引擎熔断预检查 ─────────────────────────────────────
                if self._circuit_breaker_enabled:
                    fb_can, _ = self.check_engine_available(fallback)
                    if not fb_can:
                        logger.info(
                            f"[EngineRouter] 跳过熔断中的备用引擎: {fallback.engine_name}"
                        )
                        continue

                fallback_result = await fallback.execute(task, context)

                # ── 备用引擎健康度上报 ─────────────────────────────────────
                fb_latency = fallback_result.latency_ms or 0.0
                self._report_engine_result(
                    engine=fallback,
                    success=fallback_result.success,
                    latency_ms=fb_latency,
                    error=fallback_result.error,
                )

                if fallback_result.success:
                    # 记录备用引擎 Key 成功
                    fallback_key_id = self._extract_key_id_from_result(fallback_result, fallback)
                    if fallback_key_id:
                        self._report_engine_key_success(fallback, fallback_key_id)

                    # 注入降级元数据
                    fallback_result.metadata["_fallback_from"] = (
                        decision.engine.engine_name
                    )
                    fallback_result.metadata["_fallback_reason"] = (
                        result.error
                    )
                    return fallback_result

                # 备用引擎也失败，记录其 Key 失败
                fb_key_id = self._extract_key_id_from_result(fallback_result, fallback)
                if fb_key_id:
                    self._report_engine_key_failure(fallback, fb_key_id, fallback_result.error)

        elif result.success:
            # 成功调用，记录 Key 成功
            key_id = self._extract_key_id_from_result(result, decision.engine)
            if key_id:
                self._report_engine_key_success(decision.engine, key_id)

        return result

    # -------------------------------------------------------------------------
    # Key 级别故障追踪（支持 AuthProfile 引擎）
    # -------------------------------------------------------------------------

    def _extract_key_id_from_result(
        self, result: ExecutionResult, engine: ExecutionEngine,
    ) -> str | None:
        """从执行结果中提取 key_id"""
        return result.metadata.get("key_id")

    def _report_engine_key_failure(
        self, engine: ExecutionEngine, key_id: str | None,
        error: str | None,
    ) -> None:
        """
        通知引擎某 Key 失败（触发退避）

        Args:
            engine:  引擎实例
            key_id:  失败的 Key ID
            error:   错误信息（用于判断是否可重试）
        """
        if key_id and hasattr(engine, "_report_api_failure"):
            retryable = False
            if error:
                err_lower = error.lower()
                retryable = any(kw in err_lower for kw in [
                    "rate limit", "429", "500", "502", "503", "504",
                    "timeout", "connection", "temporary", "unavailable",
                ])
            engine._report_api_failure(key_id, retryable=retryable)
            logger.debug(
                f"[EngineRouter] 通知引擎 {engine.engine_name} Key {key_id} 失败 "
                f"(retryable={retryable})"
            )

    def _report_engine_key_success(
        self, engine: ExecutionEngine, key_id: str | None,
    ) -> None:
        """通知引擎某 Key 调用成功（重置退避状态）"""
        if key_id and hasattr(engine, "_report_api_success"):
            engine._report_api_success(key_id)
            logger.debug(
                f"[EngineRouter] 通知引擎 {engine.engine_name} Key {key_id} 成功，退避重置"
            )

    # -------------------------------------------------------------------------
    # 内部工具
    # -------------------------------------------------------------------------

    def _get_fallback_engines(
        self,
        ctx: RoutingContext,
        exclude: str,
    ) -> List[ExecutionEngine]:
        """
        获取备用引擎列表

        按以下优先级排序:
        1. 与主引擎能力互补的引擎
        2. 默认引擎（如果不同于主引擎）
        3. 其他可用引擎
        """
        candidates = [
            (name, eng)
            for name, eng in self._engines.items()
            if name != exclude
        ]

        fallbacks: List[ExecutionEngine] = []
        seen: Set[str] = set()

        # 第一顺位：默认引擎
        if self._default_engine and self._default_engine != exclude:
            if self._default_engine in self._engines:
                fallbacks.append(self._engines[self._default_engine])
                seen.add(self._default_engine)

        # 第二顺位：能力互补引擎
        for name, eng in candidates:
            if name in seen:
                continue
            # 选择与主引擎 capabilities 不同的引擎
            fallbacks.append(eng)
            seen.add(name)
            if len(fallbacks) >= 2:
                break

        return fallbacks

    def _record_route(self, decision: RoutingDecision) -> None:
        """记录路由统计"""
        strategy = decision.strategy.value
        self._stats["strategy_counts"][strategy] = (
            self._stats["strategy_counts"].get(strategy, 0) + 1
        )
        engine_name = decision.engine.engine_name
        self._stats["engine_usage"][engine_name] = (
            self._stats["engine_usage"].get(engine_name, 0) + 1
        )

    def get_stats(self) -> Dict[str, Any]:
        """获取路由统计"""
        return {
            "total_routes": self._stats["total_routes"],
            "strategy_counts": self._stats["strategy_counts"],
            "engine_usage": self._stats["engine_usage"],
            "registered_engines": list(self._engines.keys()),
            "default_engine": self._default_engine,
            "rule_count": len(self._rules),
            "circuit_rejections": self._stats.get("circuit_rejections", 0),
        }

    # -------------------------------------------------------------------------
    # Phase 2: 健康度报告 API
    # -------------------------------------------------------------------------

    def get_health_report(
        self,
        models: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        生成模型健康度报告（供监控/运维使用）

        Args:
            models: 要报告的模型列表（None = 所有已知模型）

        Returns:
            Dict: generate_health_report() 的完整报告
        """
        return generate_health_report(
            models=models,
            persist_path=self._health_registry_path,
        )

    def get_circuit_breaker_snapshots(
        self,
        engine_names: Optional[List[str]] = None,
    ) -> Dict[str, Dict[str, Any]]:
        """
        获取指定引擎的熔断器快照

        Args:
            engine_names: 引擎名列表（None = 所有引擎）

        Returns:
            Dict: engine_name → snapshot dict
        """
        result = {}
        targets = engine_names or list(self._engines.keys())

        for name in targets:
            if name in self._engines:
                engine = self._engines[name]
                model = self._resolve_engine_model(engine)
                snap = self.circuit_breaker.get_snapshot(model)
                result[name] = {
                    "model": model,
                    "state": snap.state.value,
                    "failures_in_window": snap.failures_in_window,
                    "total_rejections": snap.total_rejections,
                    "remaining_open_time": round(snap.remaining_open_time, 2),
                }

        return result

    def force_circuit_open(
        self,
        engine_name: str,
        reason: str = "manual",
    ) -> bool:
        """
        手动触发熔断（紧急降级某个引擎）

        Args:
            engine_name: 引擎名
            reason: 原因说明

        Returns:
            bool: 是否成功触发
        """
        if engine_name not in self._engines:
            return False
        engine = self._engines[engine_name]
        model = self._resolve_engine_model(engine)
        self.circuit_breaker.force_open(model, reason=reason)
        logger.warning(
            f"[EngineRouter] 手动触发熔断: engine={engine_name}, model={model}, reason={reason}"
        )
        return True

    def force_circuit_close(self, engine_name: str) -> bool:
        """
        手动恢复熔断（解除某个引擎的熔断）

        Args:
            engine_name: 引擎名

        Returns:
            bool: 是否成功恢复
        """
        if engine_name not in self._engines:
            return False
        engine = self._engines[engine_name]
        model = self._resolve_engine_model(engine)
        self.circuit_breaker.force_close(model)
        self.health_registry.reset_model(model)
        logger.info(f"[EngineRouter] 手动恢复熔断: engine={engine_name}, model={model}")
        return True
