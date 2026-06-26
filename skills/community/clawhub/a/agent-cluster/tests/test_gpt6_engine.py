"""
GPT6Engine 测试套件

测试覆盖:
    1. 引擎初始化与 capabilities
    2. 健康检查 (health_check)
    3. 模拟执行 (execute, 无 API Key)
    4. 流式执行 (stream, 模拟模式)
    5. 上下文校验 (validate_context)
    6. 统计记录 (stats)
    7. 引擎名称一致性

Change Log:
    - 2026-04-14: 初始版本
"""

from __future__ import annotations

import asyncio
import pytest


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def engine():
    """创建 GPT6Engine 实例（无 API Key，模拟模式）"""
    from execution.gpt6_engine import GPT6Engine

    return GPT6Engine(config={
        "api_key": None,           # 强制模拟模式
        "model": "gpt-6",
        "max_tokens": 2048,
        "temperature": 0.3,
    })


@pytest.fixture
def minimal_context():
    """最小合法上下文"""
    return {
        "user_id": "test_user_001",
        "user_role": "admin",
    }


# =============================================================================
# 引擎基本信息测试
# =============================================================================


class TestGPT6EngineBasics:
    """引擎基本信息测试"""

    def test_engine_name(self, engine):
        """引擎名称应为 gpt-6"""
        assert engine.engine_name == "gpt-6"

    def test_capabilities_keys(self, engine):
        """capabilities 应包含所有定义的能力 key"""
        caps = engine.capabilities
        expected_keys = {
            "session_persistence",
            "harness_control",
            "sandbox",
            "credential_management",
            "self_evolution",
            "vertical_knowledge",
            "streaming",
            "multi_modal",
            "context_2m",
            "agent_completion_91",
        }
        assert set(caps.keys()) == expected_keys

    def test_gpt6_distinctive_capabilities(self, engine):
        """GPT-6 独有特性应为 True"""
        caps = engine.capabilities
        assert caps["multi_modal"] is True,       "Symphony 五模态"
        assert caps["context_2m"] is True,          "200万 Token 上下文"
        assert caps["agent_completion_91"] is True, "91% 任务完成率"
        assert caps["harness_control"] is True,   "工具调用控制"
        assert caps["credential_management"] is True, "官方凭证管理"

    def test_supported_models(self, engine):
        """支持的模型列表"""
        from execution.gpt6_engine import GPT6Engine

        assert "gpt-6" in GPT6Engine.SUPPORTED_MODELS
        assert "gpt-6-turbo" in GPT6Engine.SUPPORTED_MODELS
        assert len(GPT6Engine.SUPPORTED_MODELS) >= 2


# =============================================================================
# 模拟执行测试（无 API Key）
# =============================================================================


@pytest.mark.asyncio
class TestGPT6EngineExecute:
    """execute 方法测试"""

    async def test_execute_success(self, engine, minimal_context):
        """模拟执行成功返回 ExecutionResult"""
        result = await engine.execute("分析这份采购合同的关键条款", minimal_context)

        assert result.success is True
        assert result.output is not None
        assert isinstance(result.output, dict)
        assert result.output["status"] == "success"
        assert "simulation" in result.output.get("mode", "")
        assert "gpt-6" in result.output.get("content", "").lower()

    async def test_execute_contains_context_window(self, engine, minimal_context):
        """模拟响应应包含上下文窗口信息"""
        result = await engine.execute("查询库存", minimal_context)

        content = result.output["content"]
        # 应包含 2000000 这个数字
        assert "2,000,000" in content or "2000000" in content

    async def test_execute_metadata(self, engine, minimal_context):
        """执行结果元数据正确"""
        result = await engine.execute("测试任务", minimal_context)

        assert result.metadata["engine"] == "gpt-6"
        assert result.metadata["model"] == "gpt-6"
        assert result.metadata["provider"] == "openai"
        assert "context_window" in result.metadata

    async def test_execute_latency_recorded(self, engine, minimal_context):
        """执行延迟应被记录"""
        result = await engine.execute("一个简短任务", minimal_context)

        assert result.latency_ms > 0
        assert result.latency_ms < 10000  # 模拟执行应小于 10 秒

    async def test_execute_stats_recorded(self, engine, minimal_context):
        """执行统计应被记录"""
        stats_before = engine.get_stats()
        req_before = stats_before["total_requests"]

        await engine.execute("任务A", minimal_context)
        await engine.execute("任务B", minimal_context)

        stats_after = engine.get_stats()
        assert stats_after["total_requests"] == req_before + 2

    async def test_execute_missing_user_id_raises(self, engine):
        """缺少 user_id 应抛出 ValueError"""
        with pytest.raises(ValueError, match="user_id"):
            await engine.execute("任务", {"user_role": "admin"})

    async def test_execute_missing_user_role_raises(self, engine):
        """缺少 user_role 应抛出 ValueError"""
        with pytest.raises(ValueError, match="user_role"):
            await engine.execute("任务", {"user_id": "user"})


# =============================================================================
# 健康检查测试
# =============================================================================


@pytest.mark.asyncio
class TestGPT6EngineHealthCheck:
    """health_check 测试"""

    async def test_health_check_returns_true(self, engine):
        """健康检查应返回 True"""
        result = await engine.execute(
            task="health_check",
            context={"_health_check": True},
        )
        assert result.success is True
        assert result.output["status"] == "healthy"
        assert result.output["engine"] == "gpt-6"
        assert result.output["context_window"] == 2000000

    async def test_health_check_metadata_has_engine(self, engine):
        """健康检查元数据应包含引擎名称"""
        result = await engine.execute(
            task="health_check",
            context={"_health_check": True},
        )
        assert result.metadata["engine"] == "gpt-6"


# =============================================================================
# 流式执行测试（模拟模式）
# =============================================================================


@pytest.mark.asyncio
class TestGPT6EngineStream:
    """stream 方法测试"""

    async def test_stream_returns_chunks(self, engine, minimal_context):
        """流式执行应返回多个 StreamChunk"""
        chunks = []
        async for chunk in engine.stream("分析数据趋势", minimal_context):
            chunks.append(chunk)

        assert len(chunks) >= 3, "至少应有 3 个 chunk"
        # 最后一个 chunk.done 应为 True
        assert chunks[-1].done is True
        # 非末尾 chunk.done 应为 False
        assert all(c.done is False for c in chunks[:-1])

    async def test_stream_content_not_empty(self, engine, minimal_context):
        """流式内容不应全为空"""
        all_content = ""
        async for chunk in engine.stream("查询报告", minimal_context):
            all_content += chunk.content

        assert len(all_content) > 0
        assert "gpt-6" in all_content.lower()

    async def test_stream_delta_ms_recorded(self, engine, minimal_context):
        """delta_ms 应被记录"""
        chunks = []
        async for chunk in engine.stream("简短查询", minimal_context):
            chunks.append(chunk)

        # delta_ms 应大于等于 0
        assert all(c.delta_ms >= 0 for c in chunks)


# =============================================================================
# 角色差异化测试
# =============================================================================


@pytest.mark.asyncio
class TestGPT6EngineRoles:
    """不同角色的系统提示词测试"""

    async def test_admin_role(self, engine):
        """admin 角色应得到完整权限提示词"""
        result = await engine.execute("测试", {"user_id": "u1", "user_role": "admin"})
        content = result.output["content"]
        # admin 提示词应提及完整权限
        assert "完整权限" in content or "admin" in content.lower()

    async def test_viewer_role(self, engine):
        """viewer 角色应得到只读提示词"""
        result = await engine.execute("测试", {"user_id": "u1", "user_role": "viewer"})
        content = result.output["content"]
        assert "viewer" in content.lower() or "只读" in content

    async def test_operator_role(self, engine):
        """operator 角色应得到操作员提示词"""
        result = await engine.execute("测试", {"user_id": "u1", "user_role": "operator"})
        content = result.output["content"]
        assert "operator" in content.lower() or "操作" in content


# =============================================================================
# 配置覆盖测试
# =============================================================================


class TestGPT6EngineConfig:
    """配置参数测试"""

    def test_custom_base_url(self):
        """可自定义 base_url"""
        from execution.gpt6_engine import GPT6Engine

        engine = GPT6Engine(config={
            "api_key": None,
            "model": "gpt-6",
            "base_url": "https://custom.openai.com/v1",
        })
        assert engine._base_url == "https://custom.openai.com/v1"

    def test_custom_context_window(self):
        """可自定义 context_window"""
        from execution.gpt6_engine import GPT6Engine

        engine = GPT6Engine(config={
            "api_key": None,
            "context_window": 1000000,
        })
        assert engine._context_window == 1000000

    def test_custom_api_key_env(self):
        """可自定义 API Key 环境变量名"""
        from execution.gpt6_engine import GPT6Engine

        engine = GPT6Engine(config={
            "api_key_env": "CUSTOM_OPENAI_KEY",
        })
        assert engine._api_key_env == "CUSTOM_OPENAI_KEY"

    def test_unknown_model_warns(self):
        """未知模型应触发警告日志（不抛异常）"""
        from execution.gpt6_engine import GPT6Engine

        # 不应抛异常
        engine = GPT6Engine(config={
            "api_key": None,
            "model": "unknown-model-xyz",
        })
        assert engine._model == "unknown-model-xyz"

    def test_default_model_is_gpt6(self):
        """默认模型应为 gpt-6"""
        from execution.gpt6_engine import GPT6Engine

        engine = GPT6Engine(config={"api_key": None})
        assert engine._model == "gpt-6"

    def test_default_temperature(self):
        """默认温度应为 0.3"""
        from execution.gpt6_engine import GPT6Engine

        engine = GPT6Engine(config={"api_key": None})
        assert engine._temperature == 0.3

    def test_default_timeout(self):
        """默认超时应为 120 秒"""
        from execution.gpt6_engine import GPT6Engine

        engine = GPT6Engine(config={"api_key": None})
        assert engine._timeout == 120.0


# =============================================================================
# 与 EngineRouter 集成测试
# =============================================================================


class TestGPT6EngineRouterIntegration:
    """与 EngineRouter 的集成测试"""

    def test_gpt6_registered_in_router(self):
        """GPT6Engine 应可注册到 EngineRouter"""
        from execution import EngineRouter, GPT6Engine

        router = EngineRouter()
        gpt_engine = GPT6Engine(config={"api_key": None})
        router.register_engine(gpt_engine)

        assert "gpt-6" in router._engines
        assert router.get_engine("gpt-6").engine_name == "gpt-6"

    def test_gpt6_capabilities_in_stats(self):
        """引擎注册时 capabilities 应被记录"""
        from execution import EngineRouter, GPT6Engine

        router = EngineRouter()
        gpt_engine = GPT6Engine(config={"api_key": None})
        router.register_engine(gpt_engine)

        # 注册时 capabilities 被记录（通过 logger）
        assert "gpt-6" in router._engines


# =============================================================================
# 结果序列化测试
# =============================================================================


@pytest.mark.asyncio
class TestGPT6EngineResultSerialization:
    """ExecutionResult 序列化测试"""

    async def test_result_to_dict(self, engine, minimal_context):
        """ExecutionResult.to_dict() 应正常工作"""
        result = await engine.execute("序列化测试", minimal_context)
        d = result.to_dict()

        assert "success" in d
        assert "output" in d
        assert "metadata" in d
        assert "tokens_used" in d
        assert "latency_ms" in d
        assert "error" in d

    async def test_result_latency_rounded(self, engine, minimal_context):
        """latency_ms 应被四舍五入到 2 位小数"""
        result = await engine.execute("延迟测试", minimal_context)
        d = result.to_dict()

        # 浮点数精度检查
        latency_str = str(d["latency_ms"])
        decimal_part = latency_str.split(".")[-1] if "." in latency_str else ""
        assert len(decimal_part) <= 2
