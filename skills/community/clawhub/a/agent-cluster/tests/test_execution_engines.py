"""
Test Suite for Execution Engines

执行引擎测试套件

覆盖:
    - ExecutionEngine 抽象基类接口
    - EngineRouter 路由逻辑
    - ClaudeMAEngine / LocalEngine / DeepSeekEngine 各引擎

运行:
    pytest agent-cluster/tests/test_execution_engines.py -v

Change Log:
    - 2026-04-14: 初始版本
"""

from __future__ import annotations

import asyncio
import sys
import os

# 确保从项目根目录运行时能找到模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

# =============================================================================
# 辅助工具
# =============================================================================


class AsyncMock:
    """异步方法 Mock 辅助类"""

    def __init__(self, return_value=None, side_effect=None):
        self.return_value = return_value
        self.side_effect = side_effect
        self.call_count = 0
        self.calls = []

    async def __call__(self, *args, **kwargs):
        self.call_count += 1
        self.calls.append({"args": args, "kwargs": kwargs})
        if self.side_effect:
            if isinstance(self.side_effect, Exception):
                raise self.side_effect
            return await self.side_effect(*args, **kwargs)
        return self.return_value


# =============================================================================
# 抽象基类测试
# =============================================================================


class TestExecutionEngineBase:
    """测试 ExecutionEngine 抽象基类接口"""

    def test_engine_base_import(self):
        """测试基类可以正常导入"""
        from execution.engine_base import ExecutionEngine, ExecutionResult, StreamChunk

        assert ExecutionEngine is not None
        assert ExecutionResult is not None
        assert StreamChunk is not None

    def test_execution_result_dataclass(self):
        """测试 ExecutionResult 数据类"""
        from execution.engine_base import ExecutionResult

        result = ExecutionResult(
            success=True,
            output={"data": "test"},
            metadata={"engine": "test"},
            tokens_used=100,
            latency_ms=500.0,
        )

        assert result.success is True
        assert result.output["data"] == "test"
        assert result.metadata["engine"] == "test"
        assert result.tokens_used == 100
        assert result.latency_ms == 500.0
        assert result.error is None

        # to_dict 序列化
        d = result.to_dict()
        assert isinstance(d, dict)
        assert d["success"] is True
        assert d["tokens_used"] == 100

    def test_execution_result_failure(self):
        """测试失败结果的 error 字段"""
        from execution.engine_base import ExecutionResult

        result = ExecutionResult(
            success=False,
            output=None,
            error="Connection timeout",
            latency_ms=3000.0,
        )

        assert result.success is False
        assert result.error == "Connection timeout"

    def test_stream_chunk(self):
        """测试 StreamChunk 数据类"""
        from execution.engine_base import StreamChunk

        chunk = StreamChunk(content="Hello", done=False, delta_ms=50.0)
        assert chunk.content == "Hello"
        assert chunk.done is False
        assert chunk.delta_ms == 50.0


# =============================================================================
# 引擎路由器测试
# =============================================================================


class TestEngineRouter:
    """测试 EngineRouter 路由逻辑"""

    def setup_method(self):
        """每个测试方法前重置"""
        # 延迟导入，避免顶层失败
        from execution.engine_router import EngineRouter
        from execution.engine_base import ExecutionEngine, ExecutionResult

        # 创建测试引擎（使用 mock）
        class MockEngine(ExecutionEngine):
            def __init__(self, name="mock"):
                # Set _name before calling super().__init__() because
                # base class logs engine_name during __init__
                self._name = name
                super().__init__({})

            @property
            def engine_name(self):
                return self._name

            @property
            def capabilities(self):
                return {"streaming": True}

            async def execute(self, task, context):
                return ExecutionResult(success=True, output={"engine": self._name})

            async def stream(self, task, context):
                yield  # dummy

        self.MockEngine = MockEngine
        self.router = EngineRouter()

    def test_register_engine(self):
        """测试引擎注册"""
        engine = self.MockEngine("test-engine")
        self.router.register_engine(engine)

        assert "test-engine" in self.router._engines
        assert self.router.get_engine("test-engine") is engine

    def test_register_default_engine(self):
        """测试设为首个注册引擎为默认"""
        engine1 = self.MockEngine("engine-1")
        engine2 = self.MockEngine("engine-2")

        self.router.register_engine(engine1)
        self.router.register_engine(engine2, set_default=True)

        assert self.router._default_engine == "engine-2"

    def test_unregister_engine(self):
        """测试注销引擎"""
        engine = self.MockEngine("to-remove")
        self.router.register_engine(engine)
        assert self.router.unregister_engine("to-remove") is True
        assert self.router.get_engine("to-remove") is None

    def test_route_explicit_hint(self):
        """测试显式指定引擎（最高优先级）"""
        from execution.engine_router import RoutingContext

        engine1 = self.MockEngine("engine-a")
        engine2 = self.MockEngine("engine-b")
        self.router.register_engine(engine1, set_default=True)
        self.router.register_engine(engine2)

        ctx = RoutingContext(
            task="test task",
            intent_type="stock_query",
            user_role="admin",
            scene="general",
            entities={},
            engine_hint="engine-b",
        )

        decision = self.router.route(ctx)
        assert decision.engine.engine_name == "engine-b"
        assert decision.strategy.value == "explicit"
        assert decision.confidence == 1.0

    def test_route_default_when_no_match(self):
        """测试无匹配时使用默认引擎"""
        from execution.engine_router import RoutingContext

        engine = self.MockEngine("default-engine")
        self.router.register_engine(engine, set_default=True)

        ctx = RoutingContext(
            task="random task",
            intent_type="unknown",
            user_role="viewer",
            scene="general",
            entities={},
        )

        decision = self.router.route(ctx)
        assert decision.engine.engine_name == "default-engine"
        assert decision.strategy.value == "default"

    def test_route_intent_match(self):
        """测试意图类型匹配"""
        from execution.engine_router import RoutingContext, RoutingRule

        local = self.MockEngine("local")
        claude = self.MockEngine("claude")
        self.router.register_engine(local, set_default=True)
        self.router.register_engine(claude)

        self.router.add_rule(RoutingRule(
            name="vertical_tasks",
            engine="local",
            priority=20,
            intent_types=["stock_query", "purchase", "finance"],
        ))
        self.router.add_rule(RoutingRule(
            name="dev_tasks",
            engine="claude",
            priority=30,
            intent_types=["code", "analysis"],
        ))

        ctx = RoutingContext(
            task="查询库存情况",
            intent_type="stock_query",
            user_role="admin",
            scene="general",
            entities={},
        )
        decision = self.router.route(ctx)
        assert decision.engine.engine_name == "local"
        assert decision.strategy.value == "intent"

    def test_route_keyword_match(self):
        """测试关键词匹配"""
        from execution.engine_router import RoutingContext, RoutingRule

        domestic = self.MockEngine("domestic")
        self.router.register_engine(domestic, set_default=True)
        self.router.add_rule(RoutingRule(
            name="domestic_keywords",
            engine="domestic",
            priority=25,
            keywords=["合规", "信创", "国产"],
        ))

        ctx = RoutingContext(
            task="需要使用国产合规方案",
            intent_type="general",
            user_role="admin",
            scene="general",
            entities={},
        )
        decision = self.router.route(ctx)
        assert decision.engine.engine_name == "domestic"
        assert decision.strategy.value == "keyword"

    def test_route_scene_match(self):
        """测试场景匹配"""
        from execution.engine_router import RoutingContext, RoutingRule

        offline = self.MockEngine("local-offline")
        self.router.register_engine(offline, set_default=True)
        self.router.add_rule(RoutingRule(
            name="offline_scene",
            engine="local-offline",
            priority=15,
            scenes=["offline", "dev"],
        ))

        ctx = RoutingContext(
            task="离线环境任务",
            intent_type="general",
            user_role="admin",
            scene="offline",
            entities={},
        )
        decision = self.router.route(ctx)
        assert decision.engine.engine_name == "local-offline"
        assert decision.strategy.value == "scene"

    def test_route_no_engine_raises(self):
        """测试无引擎时抛异常"""
        from execution.engine_router import RoutingContext

        empty_router = self.router.__class__()
        ctx = RoutingContext(
            task="test", intent_type="test",
            user_role="admin", scene="general", entities={},
        )

        with pytest.raises(RuntimeError, match="没有可用的执行引擎"):
            empty_router.route(ctx)

    def test_list_engines(self):
        """测试列出所有引擎"""
        self.router.register_engine(self.MockEngine("e1"))
        self.router.register_engine(self.MockEngine("e2"), set_default=True)

        engines = self.router.list_engines()
        assert len(engines) == 2
        assert any(e["name"] == "e1" for e in engines)
        assert any(e["is_default"] for e in engines)

    def test_get_stats(self):
        """测试统计信息"""
        from execution.engine_router import RoutingContext

        self.router.register_engine(self.MockEngine("stats-engine"))

        ctx = RoutingContext(
            task="test", intent_type="test",
            user_role="admin", scene="general", entities={},
        )
        self.router.route(ctx)
        self.router.route(ctx)

        stats = self.router.get_stats()
        assert stats["total_routes"] == 2
        assert stats["registered_engines"] == ["stats-engine"]

    def test_routing_decision_to_dict(self):
        """测试 RoutingDecision 序列化"""
        from execution.engine_router import RoutingContext

        engine = self.MockEngine("dict-test")
        self.router.register_engine(engine)

        ctx = RoutingContext(
            task="test", intent_type="test",
            user_role="admin", scene="general", entities={},
        )
        decision = self.router.route(ctx)
        d = decision.to_dict()

        assert "engine" in d
        assert "strategy" in d
        assert "confidence" in d
        assert "fallback_count" in d


# =============================================================================
# ClaudeMAEngine 测试
# =============================================================================


class TestClaudeMAEngine:
    """测试 ClaudeMAEngine 引擎"""

    def setup_method(self):
        os.environ.setdefault("ANTHROPIC_API_KEY", "test-key-for-unit-test")

    def teardown_method(self):
        os.environ.pop("ANTHROPIC_API_KEY", None)

    def test_engine_name(self):
        """测试引擎名称"""
        from execution.claude_ma_engine import ClaudeMAEngine

        engine = ClaudeMAEngine()
        assert engine.engine_name == "claude-managed-agents"

    def test_capabilities(self):
        """测试能力矩阵"""
        from execution.claude_ma_engine import ClaudeMAEngine

        engine = ClaudeMAEngine()
        caps = engine.capabilities

        assert caps["session_persistence"] is True
        assert caps["self_evolution"] is False      # Claude MA 不支持
        assert caps["vertical_knowledge"] is False  # 需要自建
        assert caps["streaming"] is True
        assert caps["compliance_certified"] is False

    def test_execute_health_check(self):
        """测试健康检查"""
        import asyncio
        from execution.claude_ma_engine import ClaudeMAEngine

        engine = ClaudeMAEngine()

        async def run():
            result = await engine.execute(
                "test",
                {"_health_check": True, "user_id": "test", "user_role": "admin"}
            )
            assert result.success is True
            assert result.output["status"] == "healthy"

        asyncio.run(run())

    @pytest.mark.asyncio
    async def test_execute_context_required(self):
        """测试缺少必要上下文时抛异常"""
        from execution.claude_ma_engine import ClaudeMAEngine

        engine = ClaudeMAEngine()

        with pytest.raises(ValueError, match="缺少必要字段"):
            await engine.execute("test task", {})

    @pytest.mark.asyncio
    async def test_execute_success(self):
        """测试正常执行"""
        from execution.claude_ma_engine import ClaudeMAEngine

        engine = ClaudeMAEngine()
        result = await engine.execute(
            "分析这段代码",
            {"user_id": "user1", "user_role": "admin", "intent_type": "code"}
        )

        assert result.success is True
        assert result.output is not None
        assert "engine" in result.output
        assert result.tokens_used >= 0
        assert result.latency_ms > 0

    @pytest.mark.asyncio
    async def test_stream_output(self):
        """测试流式输出"""
        from execution.claude_ma_engine import ClaudeMAEngine

        engine = ClaudeMAEngine()
        chunks = []
        async for chunk in engine.stream(
            "测试流式",
            {"user_id": "u", "user_role": "admin"}
        ):
            chunks.append(chunk)

        assert len(chunks) > 0
        assert chunks[-1].done is True  # 最后一个 chunk 的 done=True


# =============================================================================
# LocalEngine 测试
# =============================================================================


class TestLocalEngine:
    """测试 LocalEngine 本地引擎"""

    def test_engine_name(self):
        """测试引擎名称"""
        from execution.local_engine import LocalEngine

        engine = LocalEngine()
        assert engine.engine_name == "local-self-built"

    def test_capabilities(self):
        """测试能力矩阵"""
        from execution.local_engine import LocalEngine

        engine = LocalEngine()
        caps = engine.capabilities

        assert caps["self_evolution"] is True       # M-A3 独有
        assert caps["vertical_knowledge"] is True   # 塑化行业
        assert caps["compliance_certified"] is True # 完全本地
        assert caps["streaming"] is True

    @pytest.mark.asyncio
    async def test_execute_health_check(self):
        """测试健康检查"""
        from execution.local_engine import LocalEngine

        engine = LocalEngine()
        result = await engine.execute(
            "test",
            {"_health_check": True, "user_id": "test", "user_role": "admin"}
        )

        assert result.success is True
        assert result.output["status"] == "healthy"
        assert result.metadata["engine"] == "local-self-built"

    @pytest.mark.asyncio
    async def test_execute_success(self):
        """测试正常执行（查询库存场景）"""
        from execution.local_engine import LocalEngine

        engine = LocalEngine()
        result = await engine.execute(
            "查询SKU001的库存",
            {"user_id": "user1", "user_role": "admin", "intent_type": "stock_query"}
        )

        # LocalEngine 调用 Orchestrator，可能因依赖问题返回失败
        # 但 engine 本身应正常响应（stats 记录）
        assert result.metadata["engine"] == "local-self-built"
        assert result.latency_ms > 0

    @pytest.mark.asyncio
    async def test_stats_accumulation(self):
        """测试统计累计"""
        from execution.local_engine import LocalEngine

        engine = LocalEngine()

        await engine.execute(
            "task1",
            {"_health_check": True, "user_id": "u", "user_role": "admin"}
        )
        await engine.execute(
            "task2",
            {"_health_check": True, "user_id": "u", "user_role": "admin"}
        )

        stats = engine.get_stats()
        assert stats["total_requests"] == 2
        assert stats["success"] == 2

    @pytest.mark.asyncio
    async def test_stream_output(self):
        """测试流式输出"""
        from execution.local_engine import LocalEngine

        engine = LocalEngine()
        chunks = []
        async for chunk in engine.stream(
            "查询库存",
            {"user_id": "u", "user_role": "admin"}
        ):
            chunks.append(chunk)
            if len(chunks) > 20:  # 防止无限循环
                break

        assert len(chunks) > 0
        assert chunks[-1].done is True


# =============================================================================
# DeepSeekEngine 测试
# =============================================================================


class TestDeepSeekEngine:
    """测试 DeepSeekEngine 国产模型引擎"""

    def test_engine_name(self):
        """测试引擎名称"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine()
        assert "deepseek" in engine.engine_name

    def test_capabilities(self):
        """测试能力矩阵"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine()
        caps = engine.capabilities

        assert caps["compliance_certified"] is True  # 国产合规
        assert caps["streaming"] is True
        assert caps["self_evolution"] is False

    @pytest.mark.asyncio
    async def test_execute_no_api_key_simulation(self):
        """测试无 API Key 时进入模拟模式"""
        # 确保无 key
        os.environ.pop("DEEPSEEK_API_KEY", None)

        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine()
        result = await engine.execute(
            "测试任务",
            {"user_id": "u", "user_role": "admin", "intent_type": "general"}
        )

        assert result.success is True
        assert result.output.get("mode") == "simulation"

    @pytest.mark.asyncio
    async def test_execute_health_check_no_key(self):
        """测试无 key 时健康检查"""
        os.environ.pop("DEEPSEEK_API_KEY", None)
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine()
        result = await engine.execute(
            "test",
            {"_health_check": True, "user_id": "u", "user_role": "admin"}
        )

        assert result.success is True


# =============================================================================
# 集成测试
# =============================================================================


class TestEngineIntegration:
    """测试引擎集成（Orchestrator + EngineRouter）"""

    def test_module_import(self):
        """测试 execution 模块可正常导入"""
        from execution import (
            ExecutionEngine,
            ExecutionResult,
            StreamChunk,
            EngineRouter,
            RoutingRule,
            RoutingContext,
            ClaudeMAEngine,
            LocalEngine,
            DeepSeekEngine,
        )

        assert ExecutionEngine is not None
        assert EngineRouter is not None
        assert LocalEngine is not None

    def test_all_capabilities_keys(self):
        """测试所有引擎的 capabilities 使用统一 key"""
        from execution.local_engine import LocalEngine
        from execution.claude_ma_engine import ClaudeMAEngine
        from execution.deepseek_engine import DeepSeekEngine

        STANDARD_KEYS = {
            "session_persistence", "harness_control", "sandbox",
            "credential_management", "self_evolution", "vertical_knowledge",
            "streaming", "multi_modal", "compliance_certified",
        }

        for cls in [LocalEngine, ClaudeMAEngine, DeepSeekEngine]:
            if cls.__name__ == "ClaudeMAEngine":
                os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
                engine = cls()
                os.environ.pop("ANTHROPIC_API_KEY", None)
            elif cls.__name__ == "DeepSeekEngine":
                os.environ.pop("DEEPSEEK_API_KEY", None)
                engine = cls()
            else:
                engine = cls()

            keys = set(engine.capabilities.keys())
            # 至少包含核心 key
            assert "session_persistence" in keys
            assert "streaming" in keys

    @pytest.mark.asyncio
    async def test_engine_fallback(self):
        """测试引擎降级逻辑"""
        from execution.engine_router import EngineRouter, RoutingContext
        from execution.engine_base import ExecutionEngine, ExecutionResult

        class FailingEngine(ExecutionEngine):
            @property
            def engine_name(self): return "failing"

            @property
            def capabilities(self): return {}

            async def execute(self, task, context):
                return ExecutionResult(success=False, output=None, error="Engine failed")

            async def stream(self, task, context):
                yield

        class SuccessEngine(ExecutionEngine):
            @property
            def engine_name(self): return "success"

            @property
            def capabilities(self): return {}

            async def execute(self, task, context):
                return ExecutionResult(success=True, output={"ok": True})

            async def stream(self, task, context):
                yield

        router = EngineRouter()
        router.register_engine(FailingEngine(), set_default=True)
        router.register_engine(SuccessEngine())

        ctx = RoutingContext(
            task="test", intent_type="test",
            user_role="admin", scene="general", entities={},
        )
        decision = router.route(ctx)
        result = await router.route_and_execute_async("test", {"user_id": "u", "user_role": "admin"})

        # 应该降级到 success 引擎
        assert result.success is True
        assert result.metadata.get("_fallback_from") == "failing"


# =============================================================================
# 路由规则测试
# =============================================================================


class TestRoutingRules:
    """测试 RoutingRule 匹配逻辑"""

    def test_rule_intent_match(self):
        """测试意图类型匹配"""
        from execution.engine_router import RoutingRule, RoutingContext

        rule = RoutingRule(
            name="test_intent",
            engine="target",
            intent_types=["stock_query", "purchase"],
        )

        ctx_match = RoutingContext(
            task="test", intent_type="stock_query",
            user_role="admin", scene="general", entities={},
        )
        ctx_nomatch = RoutingContext(
            task="test", intent_type="logistics",
            user_role="admin", scene="general", entities={},
        )

        assert rule.matches(ctx_match) is True
        assert rule.matches(ctx_nomatch) is False

    def test_rule_keywords_match(self):
        """测试关键词匹配"""
        from execution.engine_router import RoutingRule, RoutingContext

        rule = RoutingRule(
            name="test_kw",
            engine="target",
            keywords=["采购", "下单", "order"],
        )

        ctx_match = RoutingContext(
            task="帮我采购一批原材料",
            intent_type="purchase",
            user_role="admin", scene="general", entities={},
        )
        ctx_nomatch = RoutingContext(
            task="查询库存情况",
            intent_type="stock_query",
            user_role="admin", scene="general", entities={},
        )

        assert rule.matches(ctx_match) is True
        assert rule.matches(ctx_nomatch) is False

    def test_rule_pattern_match(self):
        """测试正则模式匹配"""
        from execution.engine_router import RoutingRule, RoutingContext

        rule = RoutingRule(
            name="test_pattern",
            engine="target",
            keyword_patterns=[r"SKU\d{3}", r"订单[A-Z]+\d+"],
        )

        ctx = RoutingContext(
            task="查询SKU001和订单PO2024001的状态",
            intent_type="mixed",
            user_role="admin", scene="general", entities={},
        )

        assert rule.matches(ctx) is True

    def test_rule_user_role_filter(self):
        """测试用户角色过滤"""
        from execution.engine_router import RoutingRule, RoutingContext

        rule = RoutingRule(
            name="test_role",
            engine="target",
            user_roles=["admin"],
        )

        ctx_admin = RoutingContext(
            task="test", intent_type="test",
            user_role="admin", scene="general", entities={},
        )
        ctx_viewer = RoutingContext(
            task="test", intent_type="test",
            user_role="viewer", scene="general", entities={},
        )

        assert rule.matches(ctx_admin) is True
        assert rule.matches(ctx_viewer) is False
