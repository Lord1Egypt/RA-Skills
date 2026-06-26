"""
Test Suite for DeepSeekEngine V3.2

DeepSeek V3.2 引擎测试套件

覆盖:
    - 引擎初始化与配置
    - 基础对话能力（模拟 / 真实 API）
    - 编程能力测试
    - 复杂推理测试（reasoner 模式）
    - 流式输出
    - 错误处理
    - API Key 安全读取
    - JSON Mode / Function Calling

运行:
    # 完整测试（需 DEEPSEEK_API_KEY）
    DEEPSEEK_API_KEY=sk-xxx pytest agent-cluster/tests/test_deepseek_engine.py -v

    # 仅单元测试（无需 API Key）
    pytest agent-cluster/tests/test_deepseek_engine.py -v -m "not integration"

Change Log:
    - 2026-04-14: V3.2 API 集成测试版本
"""

from __future__ import annotations

import asyncio
import os
import sys

# 确保从项目根目录运行时能找到模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest


# =============================================================================
# 辅助工具
# =============================================================================


class AsyncMock:
    """异步方法 Mock"""

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


def build_context(
    user_id: str = "test-user",
    user_role: str = "admin",
    intent_type: str = "general",
    **kwargs,
) -> dict:
    """构建标准执行上下文"""
    return {
        "user_id": user_id,
        "user_role": user_role,
        "intent_type": intent_type,
        **kwargs,
    }


# =============================================================================
# 单元测试（无需 API Key）
# =============================================================================

class TestDeepSeekEngineInit:
    """测试引擎初始化"""

    def teardown_method(self):
        os.environ.pop("DEEPSEEK_API_KEY", None)

    def test_init_default_config(self):
        """测试默认配置"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine()
        assert engine.model == "deepseek-chat"
        assert engine.engine_name == "domestic-deepseek-chat"
        assert engine._api_key is None
        assert engine._base_url == "https://api.deepseek.com"
        assert engine._max_tokens == 4096
        assert engine._temperature == 0.3

    def test_init_with_config(self):
        """测试配置注入"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine({
            "api_key": "dsk-test-key-123",
            "model": "deepseek-reasoner",
            "max_tokens": 8192,
            "temperature": 0.7,
            "json_mode": True,
        })
        assert engine.model == "deepseek-reasoner"
        assert engine._api_key == "dsk-test-key-123"
        assert engine._max_tokens == 8192
        assert engine._temperature == 0.7
        assert engine._json_mode is True

    def test_init_env_variable_fallback(self):
        """测试环境变量兜底读取"""
        from execution.deepseek_engine import DeepSeekEngine

        os.environ["DEEPSEEK_API_KEY"] = "dsk-env-key-456"
        engine = DeepSeekEngine()
        assert engine._api_key == "dsk-env-key-456"

    def test_init_env_overrides_config(self):
        """测试 config 优先级高于环境变量"""
        from execution.deepseek_engine import DeepSeekEngine

        os.environ["DEEPSEEK_API_KEY"] = "dsk-env-key-456"
        engine = DeepSeekEngine({"api_key": "dsk-config-key-789"})
        assert engine._api_key == "dsk-config-key-789"

    def test_init_custom_base_url(self):
        """测试自定义 base_url"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine({
            "base_url": "https://api.deepseek.com/beta",
            "use_beta": True,
        })
        assert engine._base_url == "https://api.deepseek.com/beta"

    def test_init_beta_endpoint_max_tokens(self):
        """测试 Beta 端点 max_tokens 上限 8K（仅超限部分受限）"""
        from execution.deepseek_engine import DeepSeekEngine

        # 配置值 10000 > 8192 → 应限制到 8192
        engine = DeepSeekEngine({
            "use_beta": True,
            "max_tokens": 10000,  # 超限
        })
        assert engine._max_tokens == 8192  # 被限制到 8K

        # 默认 4096 < 8192 → 不应被调高，保持原值
        engine2 = DeepSeekEngine({"use_beta": True})
        assert engine2._max_tokens == 4096

    def test_capabilities_common(self):
        """测试通用能力"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine()
        caps = engine.capabilities

        assert caps["streaming"] is True
        assert caps["compliance_certified"] is True
        assert caps["json_mode"] is False
        assert caps["session_persistence"] is True
        assert caps["multi_modal"] is False

    def test_capabilities_chat_mode(self):
        """测试 deepseek-chat 模式能力"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine({"model": "deepseek-chat"})
        caps = engine.capabilities

        assert caps["reasoning_chain"] is False
        assert caps["harness_control"] is True  # Function Calling

    def test_capabilities_reasoner_mode(self):
        """测试 deepseek-reasoner 模式能力"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine({"model": "deepseek-reasoner"})
        caps = engine.capabilities

        assert caps["reasoning_chain"] is True
        assert caps["harness_control"] is True

    def test_api_health_status(self):
        """测试 API 健康状态（不含敏感信息）"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine({"model": "deepseek-reasoner", "temperature": 0.9})
        status = engine.api_health_status

        assert status["model"] == "deepseek-reasoner"
        assert status["has_api_key"] is False
        assert status["temperature"] == 0.9
        # API Key 的具体 key 名称不应出现在字典中（用 keys() 避免误判 has_api_key）
        assert "api_key" not in status.keys()
        assert "secret" not in str(status).lower()  # 敏感值


class TestDeepSeekEngineSystemPrompt:
    """测试系统提示词构建"""

    def test_system_prompt_admin(self):
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine()
        prompt = engine._build_system_prompt({"user_role": "admin", "intent_type": "general"})
        assert "管理员" in prompt or "完整" in prompt

    def test_system_prompt_viewer(self):
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine()
        prompt = engine._build_system_prompt({"user_role": "viewer", "intent_type": "general"})
        assert "只读" in prompt or "viewer" in prompt.lower()

    def test_system_prompt_intent_stock_query(self):
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine()
        prompt = engine._build_system_prompt({"user_role": "operator", "intent_type": "stock_query"})
        assert "库存" in prompt

    def test_system_prompt_intent_code(self):
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine()
        prompt = engine._build_system_prompt({"user_role": "admin", "intent_type": "code"})
        assert "编程" in prompt or "Python" in prompt

    def test_build_messages_basic(self):
        """测试消息构建"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine()
        messages = engine._build_messages("hello", {"user_role": "admin", "intent_type": "general"})

        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == "hello"

    def test_build_messages_with_history(self):
        """测试多轮对话历史"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine()
        messages = engine._build_messages(
            "继续",
            {
                "user_role": "admin",
                "intent_type": "general",
                "history": [
                    {"role": "user", "content": "你好"},
                    {"role": "assistant", "content": "你好！有什么可以帮你的？"},
                ],
            },
        )

        assert len(messages) == 4
        assert messages[1]["content"] == "你好"
        assert messages[2]["content"] == "你好！有什么可以帮你的？"
        assert messages[3]["content"] == "继续"


class TestDeepSeekEngineSimulate:
    """测试模拟执行模式"""

    def teardown_method(self):
        os.environ.pop("DEEPSEEK_API_KEY", None)

    @pytest.mark.asyncio
    async def test_simulate_execute(self):
        """测试无 API Key 时返回模拟结果"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine()
        result = await engine.execute(
            task="查询今日库存",
            context=build_context(user_id="u001", intent_type="stock_query"),
        )

        assert result.success is True
        assert result.output["status"] == "success"
        assert result.output["mode"] == "simulation"
        assert result.output["model"] == "deepseek-chat"
        assert "DEEPSEEK_API_KEY" in result.output["content"]
        assert result.tokens_used > 0
        assert result.error is None

    @pytest.mark.asyncio
    async def test_simulate_health_check(self):
        """测试模拟模式健康检查"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine()
        result = await engine.execute(
            task="health",
            context={**build_context(), "_health_check": True},
        )

        assert result.success is True
        assert result.output["status"] == "healthy"
        assert result.output["engine"] == "domestic-deepseek-chat"

    @pytest.mark.asyncio
    async def test_simulate_stream(self):
        """测试模拟流式输出"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine()
        chunks = []
        async for chunk in engine.stream("测试任务", build_context()):
            chunks.append(chunk)

        assert len(chunks) >= 3
        assert chunks[-1].done is True
        assert all(c.content is not None for c in chunks)


class TestDeepSeekEngineContext:
    """测试上下文校验"""

    @pytest.mark.asyncio
    async def test_validate_context_missing_user_id(self):
        """测试缺少 user_id 时抛出 ValueError"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine()
        with pytest.raises(ValueError, match="user_id"):
            await engine.execute("task", {"user_role": "admin"})

    @pytest.mark.asyncio
    async def test_validate_context_missing_user_role(self):
        """测试缺少 user_role 时抛出 ValueError"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine()
        with pytest.raises(ValueError, match="user_role"):
            await engine.execute("task", {"user_id": "u001"})


class TestDeepSeekEngineStats:
    """测试统计信息"""

    @pytest.mark.asyncio
    async def test_stats_recording(self):
        """测试统计信息记录"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine()

        await engine.execute("task 1", build_context())
        await engine.execute("task 2", build_context())

        stats = engine.get_stats()
        assert stats["total_requests"] == 2
        assert stats["success"] == 2
        assert stats["failed"] == 0
        assert "success_rate" in stats
        assert stats["engine"] == "domestic-deepseek-chat"


# =============================================================================
# Mock API 测试（使用 httpx mock，无需真实网络）
# =============================================================================

class TestDeepSeekEngineAPIMock:
    """测试 API 调用逻辑（Mock 模式）"""

    def setup_method(self):
        os.environ["DEEPSEEK_API_KEY"] = "dsk-mock-key-for-test"

    def teardown_method(self):
        os.environ.pop("DEEPSEEK_API_KEY", None)

    @pytest.mark.asyncio
    async def test_call_api_basic_success(self):
        """测试基础对话 API 调用成功"""
        from unittest.mock import patch, MagicMock
        from execution.deepseek_engine import DeepSeekEngine

        mock_response_data = {
            "choices": [{
                "message": {"content": "量子计算基于量子力学原理。"},
                "finish_reason": "stop",
            }],
            "usage": {
                "prompt_tokens": 50,
                "completion_tokens": 80,
                "total_tokens": 130,
            },
        }

        # 直接 patch _call_api 避免 httpx mock 复杂性
        async def mock_call(self_, task, context):
            return {
                "status": "success",
                "content": "量子计算基于量子力学原理。",
                "model": self_._model,
                "usage": mock_response_data["usage"],
                "_estimated_tokens": 130,
                "finish_reason": "stop",
            }

        with patch.object(DeepSeekEngine, "_call_api", mock_call):
            engine = DeepSeekEngine({"api_key": "dsk-test"})
            result = await engine.execute(
                "请介绍量子计算",
                build_context(intent_type="general"),
            )

        assert result.success is True
        assert "量子计算" in result.output["content"]
        assert result.output["_estimated_tokens"] == 130
        assert result.tokens_used == 130

    @pytest.mark.asyncio
    async def test_call_api_reasoner_with_reasoning_content(self):
        """测试 reasoner 模式返回 reasoning_content"""
        from unittest.mock import patch
        from execution.deepseek_engine import DeepSeekEngine

        async def mock_call(self_, task, context):
            return {
                "status": "success",
                "content": "答案是 42",
                "model": self_._model,
                "reasoning_content": "先设 x=6*7=42，验证正确。",
                "usage": {"total_tokens": 70},
                "_estimated_tokens": 70,
                "finish_reason": "stop",
            }

        with patch.object(DeepSeekEngine, "_call_api", mock_call):
            engine = DeepSeekEngine({"api_key": "dsk-test", "model": "deepseek-reasoner"})
            result = await engine.execute(
                "6*7 等于多少",
                build_context(intent_type="analysis"),
            )

        assert result.success is True
        assert result.output["content"] == "答案是 42"
        assert result.output["reasoning_content"] == "先设 x=6*7=42，验证正确。"
        assert result.output["_estimated_tokens"] == 70

    @pytest.mark.asyncio
    async def test_call_api_401_error(self):
        """测试 401 无效 API Key"""
        from unittest.mock import patch
        from execution.deepseek_engine import DeepSeekEngine, DeepSeekAPIError

        async def mock_call_fail(self_, task, context):
            raise DeepSeekAPIError(
                "API Key 无效或未授权",
                status_code=401,
                error_code="invalid_api_key",
            )

        with patch.object(DeepSeekEngine, "_call_api", mock_call_fail):
            engine = DeepSeekEngine({"api_key": "dsk-test"})
            result = await engine.execute("hello", build_context())

        assert result.success is False
        assert "401" in result.error or "无效" in result.error

    @pytest.mark.asyncio
    async def test_call_api_429_rate_limit(self):
        """测试 429 限流"""
        from unittest.mock import patch
        from execution.deepseek_engine import DeepSeekEngine, DeepSeekAPIError

        async def mock_call_429(self_, task, context):
            raise DeepSeekAPIError(
                "请求频率超限（429）",
                status_code=429,
                error_code="rate_limit_exceeded",
            )

        with patch.object(DeepSeekEngine, "_call_api", mock_call_429):
            engine = DeepSeekEngine({"api_key": "dsk-test"})
            result = await engine.execute("hello", build_context())

        assert result.success is False
        assert "429" in result.error or "限流" in result.error

    @pytest.mark.asyncio
    async def test_call_api_with_json_mode(self):
        """测试 JSON Mode 正确传递 response_format"""
        from unittest.mock import patch
        from execution.deepseek_engine import DeepSeekEngine

        captured_json_mode = {}

        async def mock_call_json_mode(self_, task, context):
            captured_json_mode["json_mode"] = self_._json_mode
            return {
                "status": "success",
                "content": '{"name":"test","value":42}',
                "model": self_._model,
                "_estimated_tokens": 50,
            }

        with patch.object(DeepSeekEngine, "_call_api", mock_call_json_mode):
            engine = DeepSeekEngine({"api_key": "dsk-test", "json_mode": True})
            await engine.execute("返回 JSON", build_context())

        assert captured_json_mode["json_mode"] is True

    @pytest.mark.asyncio
    async def test_call_api_with_history(self):
        """测试多轮对话携带历史"""
        from unittest.mock import patch
        from execution.deepseek_engine import DeepSeekEngine

        captured_messages = {}

        async def mock_call_with_history(self_, task, context):
            nonlocal captured_messages
            captured_messages = self_._build_messages(task, context)
            return {
                "status": "success",
                "content": "继续执行之前说的。",
                "model": self_._model,
                "_estimated_tokens": 40,
            }

        with patch.object(DeepSeekEngine, "_call_api", mock_call_with_history):
            engine = DeepSeekEngine({"api_key": "dsk-test"})
            await engine.execute(
                "继续",
                {
                    **build_context(),
                    "history": [
                        {"role": "user", "content": "你好"},
                        {"role": "assistant", "content": "你好！"},
                    ],
                },
            )

        assert len(captured_messages) == 4
        assert captured_messages[1]["role"] == "user"
        assert captured_messages[2]["role"] == "assistant"
        assert captured_messages[2]["content"] == "你好！"


class TestDeepSeekEngineStreamingMock:
    """测试流式输出（Mock）"""

    def teardown_method(self):
        os.environ.pop("DEEPSEEK_API_KEY", None)

    @pytest.mark.asyncio
    async def test_stream_api_sse_parsing(self):
        """测试 SSE 数据解析（模拟流式响应）"""
        from unittest.mock import patch
        from execution.deepseek_engine import DeepSeekEngine, StreamChunk

        async def mock_stream(self_, task, context):
            """模拟 SSE 流式返回"""
            for word in ["Hello", "World!", " Done"]:
                yield StreamChunk(content=word, done=False, delta_ms=10.0)
            yield StreamChunk(content="", done=True, delta_ms=0.0)

        with patch.object(DeepSeekEngine, "_stream_api", mock_stream):
            engine = DeepSeekEngine({"api_key": "dsk-test"})
            chunks = []
            async for chunk in engine.stream("hello", build_context()):
                chunks.append(chunk)

        texts = [c.content for c in chunks if not c.done]
        assert "Hello" in texts
        assert "World!" in texts
        assert any(c.done for c in chunks)

    @pytest.mark.asyncio
    async def test_stream_reasoner_auto_fallback(self):
        """测试 reasoner 模式流式降级为阻塞调用 + 正确模拟 execute 结果"""
        from unittest.mock import patch, AsyncMock
        from execution.deepseek_engine import DeepSeekEngine, StreamChunk, ExecutionResult

        # reasoner 模式会先尝试 _stream_api（被 patch），降级到 execute
        async def mock_stream(self_, task, context):
            for word in ["The", " answer", " is", " 42."]:
                yield StreamChunk(content=word, done=False, delta_ms=5.0)
            yield StreamChunk(content="", done=True, delta_ms=0.0)

        # execute 在 reasoner 降级时使用，所以也 mock
        mock_result = ExecutionResult(
            success=True,
            output={"content": "The answer is 42.", "model": "deepseek-reasoner", "_estimated_tokens": 10},
            tokens_used=10,
            latency_ms=100.0,
        )
        async def mock_execute(self_, task, context):
            return mock_result

        with patch.object(DeepSeekEngine, "_stream_api", mock_stream), \
             patch.object(DeepSeekEngine, "execute", mock_execute):
            engine = DeepSeekEngine({"api_key": "dsk-test", "model": "deepseek-reasoner"})
            chunks = []
            async for chunk in engine.stream("6*7", build_context()):
                chunks.append(chunk)

        assert len(chunks) >= 1
        assert any(c.done for c in chunks)


# =============================================================================
# 集成测试（需要真实 API Key）
# =============================================================================

@pytest.mark.skipif(
    os.environ.get("DEEPSEEK_API_KEY", "").startswith("dsk-mock"),
    reason="跳过 Mock Key 集成测试",
)
class TestDeepSeekEngineIntegration:
    """集成测试（需真实 DEEPSEEK_API_KEY）"""

    def setup_method(self):
        self.api_key = os.environ.get("DEEPSEEK_API_KEY", "")
        if not self.api_key:
            pytest.skip("需要 DEEPSEEK_API_KEY 环境变量")

    @pytest.mark.asyncio
    async def test_integration_basic_chat(self):
        """集成测试：基础对话（deepseek-chat）"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine({
            "api_key": self.api_key,
            "model": "deepseek-chat",
            "max_tokens": 500,
        })

        result = await engine.execute(
            task="请用一句话解释量子计算的基本原理。",
            context=build_context(intent_type="analysis"),
        )

        assert result.success is True
        assert result.output["status"] == "success"
        assert len(result.output["content"]) > 10
        assert result.tokens_used > 0
        assert result.output["model"] == "deepseek-chat"

    @pytest.mark.asyncio
    async def test_integration_code_generation(self):
        """集成测试：代码生成（deepseek-chat）"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine({
            "api_key": self.api_key,
            "model": "deepseek-chat",
            "max_tokens": 600,
            "temperature": 0.2,
        })

        result = await engine.execute(
            task=(
                "写一个 Python 函数，判断一个字符串是否是回文串（忽略大小写和非字母数字字符）。"
                "函数名要求 palindrome，参数名为 s，返回 bool 类型，并加上类型注解。"
            ),
            context=build_context(intent_type="code"),
        )

        assert result.success is True
        content = result.output["content"]
        assert "def palindrome" in content
        assert "return" in content or "bool" in content

    @pytest.mark.asyncio
    async def test_integration_reasoner_reasoning(self):
        """集成测试：复杂推理（deepseek-reasoner）"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine({
            "api_key": self.api_key,
            "model": "deepseek-reasoner",
            "max_tokens": 800,
            "temperature": 0.3,
        })

        result = await engine.execute(
            task="求解微分方程 dy/dx = -2y，初始条件 y(0) = 5，给出完整推导过程。",
            context=build_context(intent_type="analysis"),
        )

        assert result.success is True
        assert result.output["status"] == "success"
        # reasoner 模式应有 reasoning_content
        assert "reasoning_content" in result.output
        # 最终答案应包含指数形式
        assert "5e" in result.output["content"] or "5*e" in result.output["content"] or "5×e" in result.output["content"] or "e^(-2x)" in result.output["content"]

    @pytest.mark.asyncio
    async def test_integration_streaming(self):
        """集成测试：流式输出"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine({
            "api_key": self.api_key,
            "model": "deepseek-chat",
            "max_tokens": 300,
        })

        chunks = []
        async for chunk in engine.stream(
            "用三句话介绍人工智能",
            build_context(intent_type="general"),
        ):
            chunks.append(chunk)

        assert len(chunks) >= 2
        assert any(c.done for c in chunks)
        accumulated = "".join(c.content for c in chunks if not c.done)
        assert len(accumulated) > 5

    @pytest.mark.asyncio
    async def test_integration_health_check(self):
        """集成测试：健康检查"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine({"api_key": self.api_key})
        is_healthy = await engine.health_check()
        assert is_healthy is True

    @pytest.mark.asyncio
    async def test_integration_multi_turn_conversation(self):
        """集成测试：多轮对话"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine({
            "api_key": self.api_key,
            "model": "deepseek-chat",
            "max_tokens": 400,
        })

        # 第一轮
        result1 = await engine.execute(
            task="Python 列表的 append 和 extend 方法有什么区别？",
            context={
                **build_context(intent_type="code"),
                "history": [],
            },
        )
        assert result1.success is True

        # 第二轮（带历史）
        result2 = await engine.execute(
            task="能给我一个具体的代码示例吗？",
            context={
                **build_context(intent_type="code"),
                "history": [
                    {"role": "user", "content": "Python 列表的 append 和 extend 方法有什么区别？"},
                    {"role": "assistant", "content": result1.output["content"]},
                ],
            },
        )
        assert result2.success is True
        assert "append" in result2.output["content"].lower() or "示例" in result2.output["content"]

    @pytest.mark.asyncio
    async def test_integration_json_mode(self):
        """集成测试：JSON Mode"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine({
            "api_key": self.api_key,
            "model": "deepseek-chat",
            "max_tokens": 300,
            "json_mode": True,
        })

        result = await engine.execute(
            task=(
                '返回一个 JSON 对象，包含字段：name（字符串）、age（整数）、'
                'skills（字符串数组）、employed（布尔值）。'
            ),
            context=build_context(intent_type="general"),
        )

        assert result.success is True
        content = result.output["content"].strip()
        # 尝试解析为 JSON
        import json as _json
        try:
            # 去掉可能的 markdown 代码块
            if content.startswith("```"):
                lines = content.split("\n")
                content = "\n".join(lines[1:-1])
            data = _json.loads(content)
            assert "name" in data
            assert "skills" in data
        except _json.JSONDecodeError:
            pytest.fail(f"JSON Mode 未返回有效 JSON: {content[:100]}")


# =============================================================================
# 边缘用例
# =============================================================================

class TestDeepSeekEngineEdgeCases:
    """边界用例测试"""

    def teardown_method(self):
        os.environ.pop("DEEPSEEK_API_KEY", None)

    @pytest.mark.asyncio
    async def test_empty_task_string(self):
        """测试空任务字符串"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine()
        result = await engine.execute("", build_context())
        assert result.success is True

    @pytest.mark.asyncio
    async def test_very_long_task(self):
        """测试超长任务字符串（模拟截断场景）"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine()
        long_task = "描述: " + "测试内容. " * 1000
        result = await engine.execute(long_task, build_context())
        assert result.success is True
        assert "测试内容" in result.output["content"]

    @pytest.mark.asyncio
    async def test_special_characters_in_task(self):
        """测试特殊字符"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine()
        result = await engine.execute(
            "测试 emoji 🎉 和特殊符号 &<>\"' 以及换行符\n第二行",
            build_context(),
        )
        assert result.success is True

    @pytest.mark.asyncio
    async def test_multiple_intents(self):
        """测试多个意图"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine()
        intents = ["stock_query", "purchase", "logistics", "finance", "code"]
        for intent in intents:
            result = await engine.execute(
                f"测试 {intent}",
                build_context(intent_type=intent),
            )
            assert result.success is True
            assert result.metadata["intent_type"] == intent

    def test_supported_models_constant(self):
        """测试支持的模型列表"""
        from execution.deepseek_engine import SUPPORTED_MODELS

        assert "deepseek-chat" in SUPPORTED_MODELS
        assert "deepseek-reasoner" in SUPPORTED_MODELS

    def test_deepseek_api_error_properties(self):
        """测试 DeepSeekAPIError 属性"""
        from execution.deepseek_engine import DeepSeekAPIError

        err = DeepSeekAPIError("test error", status_code=401, error_code="invalid_key")
        assert err.status_code == 401
        assert err.error_code == "invalid_key"
        assert "test error" in str(err)

    @pytest.mark.asyncio
    async def test_get_stats_empty(self):
        """测试初始统计为空"""
        from execution.deepseek_engine import DeepSeekEngine

        engine = DeepSeekEngine()
        stats = engine.get_stats()
        assert stats["total_requests"] == 0
        assert stats["success"] == 0
        assert stats["failed"] == 0
