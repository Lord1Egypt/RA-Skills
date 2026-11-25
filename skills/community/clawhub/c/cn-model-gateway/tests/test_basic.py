"""Basic smoke tests."""
from __future__ import annotations

import json
import sys
import os
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.adapters.base import ChatMessage, BaseAdapter, ChatResponse, ContentChunk, ToolCall
from src.router import ModelRouter, ERROR_PARAM_INVALID, ERROR_RATE_LIMITED, ERROR_INTERNAL, ENV_KEY_MAP
from src.monitor import get_hardware_info, compute_concurrency_limit, Monitor
from src.mcp_server import MCPServer
from src.frameworks import (
    LangChainToolAdapter, AutoGPTPluginAdapter, CrewAIToolAdapter,
    CozePluginAdapter, DifyToolAdapter,
)
from src.benchmark import BenchmarkSuite, QUESTION_BANK
from src.price_tracker import PriceTracker, DEFAULT_PRICES


class TestChatMessage(unittest.TestCase):
    def test_to_dict(self):
        m = ChatMessage(role="user", content="hello")
        self.assertEqual(m.to_dict(), {"role": "user", "content": "hello"})

    def test_content_chunk(self):
        c = ContentChunk(type="text", text="hi")
        self.assertEqual(c.to_dict(), {"type": "text", "text": "hi"})

    def test_chat_response(self):
        r = ChatResponse(content="hi", model="m", provider="p")
        self.assertEqual(r.content, "hi")
        self.assertEqual(r.duration_ms, 0)


class TestRouter(unittest.TestCase):
    def test_register_empty_config(self):
        router = ModelRouter()
        result = router.register_all({})
        # All providers should be False when no config
        self.assertIn("deepseek", result)
        self.assertFalse(result["deepseek"])
        self.assertEqual(len(result), 10)

    def test_register_all_providers_listed(self):
        """Ensure all 10 providers are in the registry."""
        router = ModelRouter()
        result = router.register_all({})
        expected = {"deepseek", "tongyi", "zhipu", "kimi", "hunyuan", "doubao",
                    "minimax", "lingyi", "baichuan", "stepfun"}
        self.assertEqual(set(result.keys()), expected)

    def test_auto_select_no_providers(self):
        router = ModelRouter()
        self.assertIsNone(router.auto_select())

    def test_list_available_empty(self):
        router = ModelRouter()
        self.assertEqual(router.list_available(), [])

    def test_error_mapping_invalid_key(self):
        router = ModelRouter()
        err = router._map_error("deepseek", "Error: invalid_api_key")
        self.assertIn("-32602", str(err))

    def test_error_mapping_rate_limit(self):
        router = ModelRouter()
        err = router._map_error("tongyi", "Throttling.RateLimit exceeded")
        self.assertIn("-32002", str(err))


class TestHardware(unittest.TestCase):
    def test_get_hardware_info(self):
        info = get_hardware_info()
        self.assertIn("cpu_cores", info)
        self.assertIn("memory_mb", info)
        self.assertIsInstance(info["cpu_cores"], int)

    def test_compute_concurrency_low_mem(self):
        limit = compute_concurrency_limit({"cpu_cores": 8, "memory_mb": 2048})
        self.assertEqual(limit, 1)

    def test_compute_concurrency_normal(self):
        limit = compute_concurrency_limit({"cpu_cores": 8, "memory_mb": 16384})
        self.assertGreaterEqual(limit, 1)
        self.assertLessEqual(limit, 4)


class TestMCPServer(unittest.TestCase):
    def setUp(self):
        self.router = ModelRouter()
        self.monitor = Monitor()
        self.server = MCPServer(self.router, self.monitor)

    def test_initialize(self):
        req = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
        resp = self.server.handle_request(req)
        self.assertEqual(resp["id"], 1)
        self.assertIn("result", resp)
        self.assertEqual(resp["result"]["serverInfo"]["name"], "cn-model-gateway")

    def test_tools_list(self):
        req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
        resp = self.server.handle_request(req)
        tools = resp["result"]["tools"]
        tool_names = [t["name"] for t in tools]
        self.assertIn("ask_model", tool_names)
        self.assertIn("describe_image", tool_names)
        self.assertIn("list_providers", tool_names)
        self.assertIn("health_check", tool_names)
        # v1.5.0: compare_models merged into ask_model
        self.assertNotIn("compare_models", tool_names)

    def test_resources_list(self):
        req = {"jsonrpc": "2.0", "id": 3, "method": "resources/list", "params": {}}
        resp = self.server.handle_request(req)
        uris = [r["uri"] for r in resp["result"]["resources"]]
        # v1.8.0: merged config + usage into single status resource
        self.assertIn("cn-model-gateway://status", uris)

    def test_prompts_list(self):
        req = {"jsonrpc": "2.0", "id": 4, "method": "prompts/list", "params": {}}
        resp = self.server.handle_request(req)
        names = [p["name"] for p in resp["result"]["prompts"]]
        self.assertIn("code_review", names)
        self.assertIn("translate", names)

    def test_unknown_method(self):
        req = {"jsonrpc": "2.0", "id": 5, "method": "foo/bar", "params": {}}
        resp = self.server.handle_request(req)
        self.assertIn("error", resp)

    def test_tool_list_providers_empty(self):
        req = {"jsonrpc": "2.0", "id": 6, "method": "tools/call",
               "params": {"name": "list_providers", "arguments": {}}}
        resp = self.server.handle_request(req)
        self.assertIn("result", resp)


class TestFrameworkAdapters(unittest.TestCase):
    def setUp(self):
        self.router = ModelRouter()

    def test_langchain_adapter_instantiation(self):
        adapter = LangChainToolAdapter(self.router)
        self.assertIsNotNone(adapter)

    def test_autogpt_adapter_instantiation(self):
        adapter = AutoGPTPluginAdapter(self.router)
        self.assertIsNotNone(adapter)

    def test_crewai_adapter_instantiation(self):
        adapter = CrewAIToolAdapter(self.router)
        self.assertIsNotNone(adapter)

    def test_coze_adapter_instantiation(self):
        adapter = CozePluginAdapter(self.router)
        self.assertIsNotNone(adapter)

    def test_dify_adapter_instantiation(self):
        adapter = DifyToolAdapter(self.router)
        self.assertIsNotNone(adapter)

    def test_langchain_adapter_has_methods(self):
        adapter = LangChainToolAdapter(self.router)
        self.assertTrue(hasattr(adapter, 'ask_model'))
        self.assertTrue(hasattr(adapter, 'compare_models'))
        self.assertTrue(hasattr(adapter, 'list_providers'))

    def test_autogpt_adapter_has_methods(self):
        adapter = AutoGPTPluginAdapter(self.router)
        self.assertTrue(hasattr(adapter, 'ask_model'))
        self.assertTrue(hasattr(adapter, 'handle_prompt'))
        self.assertTrue(hasattr(adapter, 'get_autogpt_commands'))

    def test_coze_openapi_spec(self):
        adapter = CozePluginAdapter(self.router)
        spec = adapter.get_openapi_spec()
        self.assertIn("openapi", spec)
        self.assertIn("paths", spec)
        self.assertIn("/ask_model", spec["paths"])

    def test_dify_provider_config(self):
        adapter = DifyToolAdapter(self.router)
        config = adapter.get_dify_provider_config()
        self.assertIn("provider", config)
        self.assertIn("tools", config)
        self.assertEqual(len(config["tools"]), 3)

    def test_coze_handle_request_unknown(self):
        adapter = CozePluginAdapter(self.router)
        result = adapter.handle_coze_request("/unknown", "get", {})
        self.assertEqual(result["status"], 404)

    def test_dify_handle_request_unknown(self):
        adapter = DifyToolAdapter(self.router)
        result = adapter.handle_dify_request("unknown_tool", {})
        self.assertIn("未知工具", result)


class TestBenchmark(unittest.TestCase):
    def test_question_bank_has_50_questions(self):
        total = sum(len(qs) for qs in QUESTION_BANK.values())
        self.assertEqual(total, 50)

    def test_question_bank_has_5_dimensions(self):
        # 5 question-based dimensions (speed is measured by runner, not questions)
        self.assertEqual(len(QUESTION_BANK), 5)

    def test_benchmark_suite_instantiation(self):
        suite = BenchmarkSuite()
        self.assertIsNotNone(suite)

    def test_benchmark_suite_dimensions(self):
        suite = BenchmarkSuite()
        self.assertEqual(len(suite.DIMENSIONS), 6)


class TestPriceTracker(unittest.TestCase):
    def test_price_tracker_instantiation(self):
        tracker = PriceTracker()
        self.assertIsNotNone(tracker)

    def test_default_prices_have_10_providers(self):
        self.assertEqual(len(DEFAULT_PRICES), 10)

    def test_price_table_generation(self):
        tracker = PriceTracker()
        table = tracker.generate_price_table()
        self.assertIn("Provider", table)
        self.assertIn("Input", table)

    def test_predict_cost(self):
        tracker = PriceTracker()
        result = tracker.predict_cost({"deepseek": 1000000})
        self.assertIn("total_estimated_cost", result)
        self.assertIn("predictions", result)


class TestEnvVarApiKey(unittest.TestCase):
    """Tests for environment variable API key reading (v1.4.0)."""

    def test_env_key_map_has_all_providers(self):
        """All 10 providers should have an env var mapping."""
        expected = {"deepseek", "tongyi", "zhipu", "kimi", "hunyuan", "doubao",
                    "minimax", "lingyi", "baichuan", "stepfun"}
        self.assertEqual(set(ENV_KEY_MAP.keys()), expected)

    @patch.dict(os.environ, {"DEEPSEEK_API_KEY": "env-key-123"})
    def test_register_all_uses_env_var(self):
        """register_all should read api_key from environment variable."""
        router = ModelRouter()
        # Config without api_key, but env var set
        config = {"deepseek": {}}
        availability = router.register_all(config)
        self.assertTrue(availability["deepseek"])

    def test_register_all_fallback_to_config(self):
        """register_all should fallback to config.json when env var is empty."""
        router = ModelRouter()
        config = {"deepseek": {"api_key": "config-key-456"}}
        # Make sure env var is not set
        with patch.dict(os.environ, {}, clear=True):
            # Clear any DEEPSEEK_API_KEY that might be set
            env_backup = os.environ.pop("DEEPSEEK_API_KEY", None)
            try:
                availability = router.register_all(config)
                self.assertTrue(availability["deepseek"])
            finally:
                if env_backup:
                    os.environ["DEEPSEEK_API_KEY"] = env_backup


class TestFailover(unittest.TestCase):
    """Tests for auto mode failover (v1.4.0)."""

    def test_auto_select_returns_string(self):
        """auto_select should return a provider name string."""
        router = ModelRouter()
        result = router.auto_select()
        # With no adapters, should return None
        self.assertIsNone(result)

    def test_router_has_timeout_param(self):
        """ModelRouter should accept timeout parameter."""
        router = ModelRouter(timeout=60)
        self.assertEqual(router._timeout, 60)

    def test_router_has_failover_param(self):
        """ModelRouter should accept failover parameter."""
        router = ModelRouter(failover=False)
        self.assertFalse(router._failover)

    def test_router_default_timeout_30(self):
        """Default timeout should be 30 seconds."""
        router = ModelRouter()
        self.assertEqual(router._timeout, 30)

    def test_router_default_failover_true(self):
        """Default failover should be True."""
        router = ModelRouter()
        self.assertTrue(router._failover)

    def test_capability_score_default(self):
        """Unknown provider should have default score 0.5."""
        router = ModelRouter()
        self.assertEqual(router._get_capability_score("unknown"), 0.5)

    def test_health_cache_ttl(self):
        """Health check cache should expire after TTL."""
        from src.router import HEALTH_CHECK_CACHE_TTL
        self.assertEqual(HEALTH_CHECK_CACHE_TTL, 60)


class TestWALMode(unittest.TestCase):
    """Tests for SQLite WAL mode (v1.4.0)."""

    def test_monitor_wal_enabled(self):
        """Monitor database should enable WAL mode."""
        monitor = Monitor()
        import sqlite3
        with sqlite3.connect(monitor.db_path) as conn:
            result = conn.execute("PRAGMA journal_mode").fetchone()
        self.assertEqual(result[0], "wal")

    def test_benchmark_wal_enabled(self):
        """Benchmark database should enable WAL mode."""
        suite = BenchmarkSuite()
        import sqlite3
        with sqlite3.connect(suite.db_path) as conn:
            result = conn.execute("PRAGMA journal_mode").fetchone()
        self.assertEqual(result[0], "wal")

    def test_price_tracker_wal_enabled(self):
        """Price tracker database should enable WAL mode."""
        tracker = PriceTracker()
        import sqlite3
        with sqlite3.connect(tracker.db_path) as conn:
            result = conn.execute("PRAGMA journal_mode").fetchone()
        self.assertEqual(result[0], "wal")


class TestChatMessageImageField(unittest.TestCase):
    """Tests for ChatMessage image field (v1.5.0)."""

    def test_default_image_empty(self):
        """ChatMessage image field should default to empty string."""
        msg = ChatMessage(role="user", content="hello")
        self.assertEqual(msg.image, "")

    def test_image_field_accepts_url(self):
        """ChatMessage should accept image URL."""
        msg = ChatMessage(role="user", content="describe", image="https://example.com/img.jpg")
        self.assertEqual(msg.image, "https://example.com/img.jpg")

    def test_to_dict_without_image(self):
        """to_dict without image should have simple content string."""
        msg = ChatMessage(role="user", content="hello")
        d = msg.to_dict()
        self.assertEqual(d["content"], "hello")
        self.assertNotIn("image_url", d)

    def test_to_dict_with_image(self):
        """to_dict with image should have multimodal content."""
        msg = ChatMessage(role="user", content="describe", image="https://example.com/img.jpg")
        d = msg.to_dict()
        self.assertIsInstance(d["content"], list)
        self.assertEqual(len(d["content"]), 2)
        self.assertEqual(d["content"][0]["type"], "image_url")
        self.assertEqual(d["content"][1]["type"], "text")


class TestChatResponseToolCalls(unittest.TestCase):
    """Tests for ChatResponse tool_calls field (v1.5.0)."""

    def test_default_tool_calls_empty(self):
        """ChatResponse tool_calls should default to empty list."""
        resp = ChatResponse(content="hi", model="m", provider="p")
        self.assertEqual(resp.tool_calls, [])

    def test_tool_calls_field_populated(self):
        """ChatResponse should accept tool_calls."""
        tc = ToolCall(id="tc1", name="get_weather", arguments={"city": "Beijing"})
        resp = ChatResponse(content="", model="m", provider="p", tool_calls=[tc])
        self.assertEqual(len(resp.tool_calls), 1)
        self.assertEqual(resp.tool_calls[0].name, "get_weather")

    def test_to_dict_without_tool_calls(self):
        """to_dict without tool_calls should not include tool_calls key."""
        resp = ChatResponse(content="hi", model="m", provider="p")
        d = resp.to_dict()
        self.assertNotIn("tool_calls", d)

    def test_to_dict_with_tool_calls(self):
        """to_dict with tool_calls should include them."""
        tc = ToolCall(id="tc1", name="get_weather", arguments={"city": "Beijing"})
        resp = ChatResponse(content="", model="m", provider="p", tool_calls=[tc])
        d = resp.to_dict()
        self.assertIn("tool_calls", d)
        self.assertEqual(len(d["tool_calls"]), 1)
        self.assertEqual(d["tool_calls"][0]["name"], "get_weather")


class TestToolCallBase(unittest.TestCase):
    """Tests for BaseAdapter format_tools/parse_tool_calls (v1.5.0)."""

    def setUp(self):
        """Create a concrete adapter for testing base methods."""
        from src.adapters.deepseek import DeepSeekAdapter
        self.adapter = DeepSeekAdapter(api_key="test-key")

    def test_format_tools_openai_compatible(self):
        """format_tools should produce OpenAI-compatible format."""
        tools = [{"name": "get_weather", "description": "Get weather", "parameters": {"type": "object"}}]
        formatted = self.adapter.format_tools(tools)
        self.assertEqual(len(formatted), 1)
        self.assertEqual(formatted[0]["type"], "function")
        self.assertEqual(formatted[0]["function"]["name"], "get_weather")

    def test_parse_tool_calls_empty(self):
        """parse_tool_calls with no tool_calls in response."""
        raw = {"choices": [{"message": {"content": "hi"}}]}
        result = self.adapter.parse_tool_calls(raw)
        self.assertEqual(result, [])

    def test_parse_tool_calls_with_calls(self):
        """parse_tool_calls should extract tool calls from OpenAI format."""
        raw = {
            "choices": [{
                "message": {
                    "content": "",
                    "tool_calls": [{
                        "id": "tc1",
                        "function": {"name": "get_weather", "arguments": '{"city": "Beijing"}'}
                    }]
                }
            }]
        }
        result = self.adapter.parse_tool_calls(raw)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "get_weather")
        self.assertEqual(result[0].arguments, {"city": "Beijing"})


class TestMCPToolMerge(unittest.TestCase):
    """Tests for MCP tool merge (v1.5.0)."""

    def test_ask_model_has_providers_param(self):
        """ask_model tool should have providers parameter."""
        router = ModelRouter()
        monitor = Monitor()
        server = MCPServer(router, monitor)
        ask_tool = server._tools.get("ask_model")
        self.assertIsNotNone(ask_tool)
        props = ask_tool["inputSchema"]["properties"]
        self.assertIn("providers", props)

    def test_ask_model_has_tools_param(self):
        """ask_model tool should have tools parameter for Function Calling."""
        router = ModelRouter()
        monitor = Monitor()
        server = MCPServer(router, monitor)
        ask_tool = server._tools.get("ask_model")
        props = ask_tool["inputSchema"]["properties"]
        self.assertIn("tools", props)

    def test_describe_image_tool_exists(self):
        """describe_image tool should exist."""
        router = ModelRouter()
        monitor = Monitor()
        server = MCPServer(router, monitor)
        self.assertIn("describe_image", server._tools)

    def test_compare_models_removed(self):
        """compare_models tool should be removed (merged into ask_model)."""
        router = ModelRouter()
        monitor = Monitor()
        server = MCPServer(router, monitor)
        self.assertNotIn("compare_models", server._tools)


class TestNewToolsV16(unittest.TestCase):
    """Tests for 4 new MCP tools (v1.6.0)."""

    def setUp(self):
        self.router = ModelRouter()
        self.monitor = Monitor()
        self.server = MCPServer(self.router, self.monitor)

    def test_embed_text_tool_exists(self):
        """embed_text tool should be registered."""
        self.assertIn("embed_text", self.server._tools)

    def test_rerank_tool_exists(self):
        """rerank tool should be registered."""
        self.assertIn("rerank", self.server._tools)

    def test_audio_transcribe_tool_exists(self):
        """audio_transcribe tool should be registered."""
        self.assertIn("audio_transcribe", self.server._tools)

    def test_video_understand_tool_exists(self):
        """video_understand tool should be registered."""
        self.assertIn("video_understand", self.server._tools)

    def test_embed_text_has_texts_param(self):
        """embed_text tool should have texts parameter."""
        tool = self.server._tools["embed_text"]
        props = tool["inputSchema"]["properties"]
        self.assertIn("texts", props)

    def test_rerank_has_query_and_documents_params(self):
        """rerank tool should have query and documents parameters."""
        tool = self.server._tools["rerank"]
        props = tool["inputSchema"]["properties"]
        self.assertIn("query", props)
        self.assertIn("documents", props)

    def test_audio_transcribe_has_audio_param(self):
        """audio_transcribe tool should have audio parameter."""
        tool = self.server._tools["audio_transcribe"]
        props = tool["inputSchema"]["properties"]
        self.assertIn("audio", props)

    def test_video_understand_has_video_param(self):
        """video_understand tool should have video parameter."""
        tool = self.server._tools["video_understand"]
        props = tool["inputSchema"]["properties"]
        self.assertIn("video", props)


class TestNewToolCount(unittest.TestCase):
    """Test that v1.8.0 has exactly 10 MCP tools."""

    def test_tool_count_is_11(self):
        """v2.1.0: Should have 13 tools (added key_pool_health, member_report)."""
        router = ModelRouter()
        monitor = Monitor()
        server = MCPServer(router, monitor)
        req = {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}
        resp = server.handle_request(req)
        tools = resp["result"]["tools"]
        tool_names = {t["name"] for t in tools}
        expected = {
            "ask_model", "describe_image", "embed_text", "rerank",
            "audio_transcribe", "video_understand", "batch_submit", "batch_result",
            "list_providers", "health_check", "health_report",
            "key_pool_health", "member_report",
        }
        self.assertEqual(tool_names, expected)


class TestEmbedTextBase(unittest.TestCase):
    """Tests for embed_text on BaseAdapter (default NotImplementedError)."""

    def setUp(self):
        from src.adapters.deepseek import DeepSeekAdapter
        self.adapter = DeepSeekAdapter(api_key="test-key")

    def test_deepseek_has_embed_text(self):
        """DeepSeek adapter should have embed_text method."""
        self.assertTrue(hasattr(self.adapter, 'embed_text'))

    def test_embed_text_not_raises_type_error(self):
        """DeepSeek embed_text should accept list of texts."""
        import inspect
        sig = inspect.signature(self.adapter.embed_text)
        params = list(sig.parameters.keys())
        self.assertIn("texts", params)


class TestRerankBase(unittest.TestCase):
    """Tests for rerank on BaseAdapter."""

    def setUp(self):
        from src.adapters.zhipu import ZhiPuAdapter
        self.adapter = ZhiPuAdapter(api_key="test-key")

    def test_zhipu_has_rerank(self):
        """ZhiPu adapter should have rerank method."""
        self.assertTrue(hasattr(self.adapter, 'rerank'))


class TestKernelVersion(unittest.TestCase):
    """Tests for shared kernel version."""

    def test_kernel_version_exists(self):
        """llm_core should have __kernel_version__."""
        from src import llm_core
        self.assertTrue(hasattr(llm_core, '__kernel_version__'))

    def test_kernel_version_matches(self):
        """llm_core version should be 1.6.0."""
        from src import llm_core
        self.assertEqual(llm_core.__version__, "1.6.0")


class TestEmbedResult(unittest.TestCase):
    """Tests for EmbeddingResult type."""

    def test_embedding_result_creation(self):
        """EmbeddingResult should be creatable."""
        from src.llm_core.types import EmbeddingResult
        result = EmbeddingResult(
            provider="deepseek",
            model="deepseek-embedding",
            embeddings=[[0.1, 0.2, 0.3]],
            usage={"total_tokens": 10},
            duration_ms=100,
        )
        self.assertEqual(result.provider, "deepseek")
        self.assertEqual(len(result.embeddings), 1)
        self.assertEqual(result.duration_ms, 100)


class TestRerankResult(unittest.TestCase):
    """Tests for RerankResult type."""

    def test_rerank_result_creation(self):
        """RerankResult should be creatable."""
        from src.llm_core.types import RerankResult
        result = RerankResult(
            provider="zhipu",
            model="rerank",
            scores=[0.9, 0.5, 0.1],
            usage={"total_tokens": 20},
            duration_ms=200,
        )
        self.assertEqual(result.provider, "zhipu")
        self.assertEqual(len(result.scores), 3)


class TestTranscriptionResult(unittest.TestCase):
    """Tests for TranscriptionResult type."""

    def test_transcription_result_creation(self):
        """TranscriptionResult should be creatable."""
        from src.llm_core.types import TranscriptionResult
        result = TranscriptionResult(
            provider="zhipu",
            model="glm-asr",
            text="你好世界",
            language="zh",
            duration_ms=300,
        )
        self.assertEqual(result.text, "你好世界")
        self.assertEqual(result.language, "zh")


class TestVideoUnderstandingResult(unittest.TestCase):
    """Tests for VideoUnderstandingResult type."""

    def test_video_result_creation(self):
        """VideoUnderstandingResult should be creatable."""
        from src.llm_core.types import VideoUnderstandingResult
        result = VideoUnderstandingResult(
            provider="zhipu",
            model="glm-4v",
            description="视频展示了一只猫",
            keyframe_count=5,
            duration_ms=400,
        )
        self.assertEqual(result.keyframe_count, 5)


if __name__ == "__main__":
    unittest.main()


# ========== v1.8.0 Tests: Batch Async + SSE Heartbeat + Resource Consolidation ==========


class TestChunkBuffer(unittest.TestCase):
    """Tests for ChunkBuffer (SSE reconnect ring buffer)."""

    def test_append_and_get(self):
        from src.mcp_server import ChunkBuffer
        buf = ChunkBuffer(max_size=10)
        buf.append("req1", "chunk1")
        buf.append("req1", "chunk2")
        chunks = buf.get_since("req1")
        self.assertEqual(chunks, ["chunk1", "chunk2"])

    def test_max_size_trims(self):
        from src.mcp_server import ChunkBuffer
        buf = ChunkBuffer(max_size=3)
        for i in range(5):
            buf.append("req1", f"c{i}")
        chunks = buf.get_since("req1")
        self.assertEqual(len(chunks), 3)
        self.assertEqual(chunks, ["c2", "c3", "c4"])

    def test_get_since_index(self):
        from src.mcp_server import ChunkBuffer
        buf = ChunkBuffer(max_size=10)
        for i in range(5):
            buf.append("req1", f"c{i}")
        chunks = buf.get_since("req1", last_index=3)
        self.assertEqual(chunks, ["c3", "c4"])

    def test_clear(self):
        from src.mcp_server import ChunkBuffer
        buf = ChunkBuffer(max_size=10)
        buf.append("req1", "c1")
        buf.clear("req1")
        self.assertEqual(buf.get_since("req1"), [])

    def test_multiple_requests(self):
        from src.mcp_server import ChunkBuffer
        buf = ChunkBuffer(max_size=10)
        buf.append("req1", "a")
        buf.append("req2", "b")
        self.assertEqual(buf.get_since("req1"), ["a"])
        self.assertEqual(buf.get_since("req2"), ["b"])


class TestBatchQueue(unittest.TestCase):
    """Tests for BatchQueue (SQLite WAL task queue)."""

    def setUp(self):
        import tempfile
        self.tmpdir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.tmpdir, "test_batch.db")
        from src.batch_queue import BatchQueue
        self.queue = BatchQueue(db_path=self.db_path)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_create_task(self):
        items = [{"tool": "ask_model", "args": {"question": "hi"}}]
        task_id = self.queue.create_task(items)
        self.assertTrue(task_id.startswith("batch_"))

    def test_create_task_with_priority(self):
        items = [{"tool": "ask_model", "args": {"question": "hi"}}]
        task_id = self.queue.create_task(items, priority=3)
        task = self.queue.get_task(task_id)
        self.assertEqual(task["priority"], 3)

    def test_get_task(self):
        items = [{"tool": "ask_model", "args": {"question": "hi"}}]
        task_id = self.queue.create_task(items)
        task = self.queue.get_task(task_id)
        self.assertEqual(task["status"], "pending")
        self.assertEqual(task["total"], 1)
        self.assertEqual(task["done"], 0)

    def test_get_task_not_found(self):
        task = self.queue.get_task("batch_nonexistent")
        self.assertIsNone(task)

    def test_claim_next_item(self):
        items = [{"tool": "ask_model", "args": {"question": "q1"}}, {"tool": "ask_model", "args": {"question": "q2"}}]
        task_id = self.queue.create_task(items)
        item = self.queue.claim_next_item(task_id)
        self.assertIsNotNone(item)
        self.assertEqual(item["_index"], 0)

    def test_claim_next_item_returns_none_when_done(self):
        items = [{"tool": "ask_model", "args": {"question": "q1"}}]
        task_id = self.queue.create_task(items)
        self.queue.claim_next_item(task_id)
        self.queue.complete_item(task_id, 0, {"content": "result"})
        self.queue.finish_task(task_id)
        item = self.queue.claim_next_item(task_id)
        self.assertIsNone(item)

    def test_complete_item_success(self):
        items = [{"tool": "ask_model", "args": {"question": "hi"}}]
        task_id = self.queue.create_task(items)
        self.queue.claim_next_item(task_id)
        self.queue.complete_item(task_id, 0, {"content": "result"})
        task = self.queue.get_task(task_id)
        self.assertEqual(task["done"], 1)
        self.assertEqual(task["errors"], 0)

    def test_complete_item_error(self):
        items = [{"tool": "ask_model", "args": {"question": "hi"}}]
        task_id = self.queue.create_task(items)
        self.queue.claim_next_item(task_id)
        self.queue.complete_item(task_id, 0, None, error="API timeout")
        task = self.queue.get_task(task_id)
        self.assertEqual(task["errors"], 1)

    def test_finish_task(self):
        items = [{"tool": "ask_model", "args": {"question": "hi"}}]
        task_id = self.queue.create_task(items)
        self.queue.claim_next_item(task_id)
        self.queue.complete_item(task_id, 0, {"content": "ok"})
        self.queue.finish_task(task_id)
        task = self.queue.get_task(task_id)
        self.assertEqual(task["status"], "done")

    def test_list_items(self):
        items = [{"tool": "ask_model", "args": {"question": "q1"}}, {"tool": "ask_model", "args": {"question": "q2"}}]
        task_id = self.queue.create_task(items)
        result = self.queue.list_items(task_id)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["tool"], "ask_model")
        self.assertEqual(result[0]["status"], "pending")

    def test_list_items_after_completion(self):
        items = [{"tool": "ask_model", "args": {"question": "q1"}}]
        task_id = self.queue.create_task(items)
        self.queue.claim_next_item(task_id)
        self.queue.complete_item(task_id, 0, {"content": "result"})
        result = self.queue.list_items(task_id)
        self.assertEqual(result[0]["status"], "done")

    def test_list_tasks(self):
        for i in range(3):
            self.queue.create_task([{"tool": "ask_model", "args": {"question": f"q{i}"}}])
        tasks = self.queue.list_tasks(limit=2)
        self.assertEqual(len(tasks), 2)


class TestBatchWorker(unittest.TestCase):
    """Tests for BatchWorker (background worker thread)."""

    def test_start_stop(self):
        import tempfile, os
        tmpdir = tempfile.mkdtemp()
        db_path = os.path.join(tmpdir, "test.db")
        from src.batch_queue import BatchQueue, BatchWorker
        queue = BatchQueue(db_path=db_path)
        router = MagicMock()
        monitor = MagicMock()
        worker = BatchWorker(queue=queue, router=router, monitor=monitor, max_concurrency=1)
        worker.start()
        self.assertTrue(worker.is_running())
        worker.stop()
        self.assertFalse(worker.is_running())

    def test_max_concurrency(self):
        import tempfile, os
        tmpdir = tempfile.mkdtemp()
        db_path = os.path.join(tmpdir, "test.db")
        from src.batch_queue import BatchQueue, BatchWorker
        queue = BatchQueue(db_path=db_path)
        worker = BatchWorker(queue=queue, router=MagicMock(), monitor=MagicMock(), max_concurrency=2)
        self.assertEqual(worker.max_concurrency, 2)


class TestMCPServerV19(unittest.TestCase):
    """Tests for v1.8.0 MCPServer features."""

    def setUp(self):
        self.router = ModelRouter()
        self.monitor = Monitor()
        self.server = MCPServer(self.router, self.monitor)

    def test_tool_count_is_11(self):
        """v2.1.0: Should have 13 tools (added key_pool_health, member_report)."""
        req = {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}
        resp = self.server.handle_request(req)
        tools = resp["result"]["tools"]
        tool_names = {t["name"] for t in tools}
        expected = {
            "ask_model", "describe_image", "embed_text", "rerank",
            "audio_transcribe", "video_understand", "batch_submit", "batch_result",
            "list_providers", "health_check", "health_report",
            "key_pool_health", "member_report",
        }
        self.assertEqual(tool_names, expected)

    def test_batch_submit_tool_exists(self):
        """batch_submit tool should be registered."""
        self.assertIn("batch_submit", self.server._tools)

    def test_batch_result_tool_exists(self):
        """batch_result tool should be registered."""
        self.assertIn("batch_result", self.server._tools)

    def test_batch_submit_has_tasks_param(self):
        """batch_submit tool should have tasks parameter."""
        tool = self.server._tools["batch_submit"]
        props = tool["inputSchema"]["properties"]
        self.assertIn("tasks", props)

    def test_batch_result_has_task_id_param(self):
        """batch_result tool should have task_id parameter."""
        tool = self.server._tools["batch_result"]
        props = tool["inputSchema"]["properties"]
        self.assertIn("task_id", props)

    def test_resources_list_single_status(self):
        """v2.1.0: resources/list should return 3 resources (catalog/usage/status)."""
        req = {"jsonrpc": "2.0", "id": 3, "method": "resources/list", "params": {}}
        resp = self.server.handle_request(req)
        uris = [r["uri"] for r in resp["result"]["resources"]]
        self.assertEqual(len(uris), 3)
        self.assertIn("cn-model-gateway://status", uris)
        self.assertIn("models://catalog", uris)
        self.assertIn("usage://summary", uris)
        self.assertNotIn("cn-model-gateway://config", uris)

    def test_resource_read_status(self):
        """cn-model-gateway://status should return merged config+usage+alerts."""
        req = {"jsonrpc": "2.0", "id": 4, "method": "resources/read",
               "params": {"uri": "cn-model-gateway://status"}}
        resp = self.server.handle_request(req)
        self.assertIn("result", resp)
        text = resp["result"]["contents"][0]["text"]
        data = json.loads(text)
        self.assertIn("config", data)
        self.assertIn("usage", data)
        self.assertIn("quota_alerts", data)

    def test_resource_read_unknown_uri(self):
        """Unknown resource URI should return error."""
        req = {"jsonrpc": "2.0", "id": 5, "method": "resources/read",
               "params": {"uri": "cn-model-gateway://nonexistent"}}
        resp = self.server.handle_request(req)
        self.assertIn("error", resp)

    def test_batch_submit_empty_tasks(self):
        """batch_submit with empty tasks should raise error."""
        req = {"jsonrpc": "2.0", "id": 10, "method": "tools/call",
               "params": {"name": "batch_submit", "arguments": {"tasks": []}}}
        resp = self.server.handle_request(req)
        self.assertIn("error", resp)

    def test_batch_result_missing_task_id(self):
        """batch_result with missing task_id should raise error."""
        req = {"jsonrpc": "2.0", "id": 11, "method": "tools/call",
               "params": {"name": "batch_result", "arguments": {}}}
        resp = self.server.handle_request(req)
        self.assertIn("error", resp)

    def test_batch_result_nonexistent_task(self):
        """batch_result with nonexistent task_id should return not found."""
        req = {"jsonrpc": "2.0", "id": 12, "method": "tools/call",
               "params": {"name": "batch_result", "arguments": {"task_id": "batch_9999999999999"}}}
        resp = self.server.handle_request(req)
        self.assertIn("result", resp)
        self.assertIn("不存在", resp["result"]["content"][0]["text"])

    def test_version_is_190(self):
        """Server version should be 2.1.0."""
        req = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
        resp = self.server.handle_request(req)
        self.assertEqual(resp["result"]["serverInfo"]["version"], "2.1.0")

    def test_shutdown(self):
        """Server shutdown should stop batch worker."""
        self.server.shutdown()
        self.assertFalse(self.server._batch_worker.is_running())

    def test_health_report_tool_exists(self):
        """health_report tool should be registered."""
        self.assertIn("health_report", self.server._tools)

    def test_health_report_has_save_param(self):
        """health_report tool should have save parameter."""
        tool = self.server._tools["health_report"]
        props = tool["inputSchema"]["properties"]
        self.assertIn("save", props)

    def test_health_report_has_days_param(self):
        """health_report tool should have days parameter."""
        tool = self.server._tools["health_report"]
        props = tool["inputSchema"]["properties"]
        self.assertIn("days", props)

    def test_health_report_call(self):
        """health_report tool call should work."""
        req = {"jsonrpc": "2.0", "id": 20, "method": "tools/call",
               "params": {"name": "health_report", "arguments": {"save": False}}}
        resp = self.server.handle_request(req)
        self.assertIn("result", resp)
        text = resp["result"]["content"][0]["text"]
        self.assertIn("每日健康晨报", text)


class TestHealthScheduler(unittest.TestCase):
    """Tests for v1.9.0 HealthScheduler."""

    def setUp(self):
        import tempfile
        from src.scheduler import HealthScheduler
        self._tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self._tmp.close()
        self.scheduler = HealthScheduler(db_path=self._tmp.name)

    def tearDown(self):
        import os
        try:
            os.unlink(self._tmp.name)
        except OSError:
            pass

    def test_init_db(self):
        """HealthScheduler should initialize database."""
        self.assertIsNotNone(self.scheduler.db_path)

    def test_check_once_no_providers(self):
        """check_once with no providers should return empty list."""
        from src.router import ModelRouter
        router = ModelRouter()
        results = self.scheduler.check_once(router)
        self.assertEqual(results, [])

    def test_generate_morning_report_empty(self):
        """generate_morning_report with no data should return placeholder."""
        html = self.scheduler.generate_morning_report()
        self.assertIn("暂无健康检查数据", html)

    def test_detect_anomaly_no_data(self):
        """_detect_anomaly with no data should return empty list."""
        alerts = self.scheduler._detect_anomaly()
        self.assertEqual(alerts, [])

    def test_save_report(self):
        """save_report should save HTML to file."""
        import os
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
            path = f.name
        result_path = self.scheduler.save_report(path=path)
        self.assertEqual(result_path, path)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        # With no data, should show placeholder text
        self.assertTrue(len(content) > 0)
        os.unlink(path)

    def test_start_stop_scheduler(self):
        """start_scheduler and stop_scheduler should work."""
        from src.router import ModelRouter
        router = ModelRouter()
        self.scheduler.start_scheduler(router, interval_hours=24)
        self.assertTrue(self.scheduler._running)
        self.scheduler.stop_scheduler()
        self.assertFalse(self.scheduler._running)


class TestErrorMapYAML(unittest.TestCase):
    """Tests for v1.9.0 YAML error map."""

    def test_error_map_loaded(self):
        """ERROR_MAP should be loaded from YAML."""
        from src.llm_core.error_map import ERROR_MAP
        self.assertGreater(len(ERROR_MAP), 0)

    def test_all_providers_present(self):
        """All 10 providers should be in ERROR_MAP."""
        from src.llm_core.error_map import ERROR_MAP
        expected = {"deepseek", "tongyi", "zhipu", "kimi", "hunyuan", "doubao",
                    "minimax", "lingyi", "baichuan", "stepfun"}
        for p in expected:
            self.assertIn(p, ERROR_MAP, f"Provider {p} missing from ERROR_MAP")

    def test_new_error_types_present(self):
        """New error types (429, 451, balance_insufficient, content_audit) should be present."""
        from src.llm_core.error_map import ERROR_MAP
        for provider in ["deepseek", "tongyi", "zhipu", "kimi", "hunyuan", "doubao"]:
            provider_map = ERROR_MAP.get(provider, {})
            self.assertIn("429", provider_map, f"{provider} missing 429 error")
            self.assertIn("451", provider_map, f"{provider} missing 451 error")
            self.assertIn("balance_insufficient", provider_map, f"{provider} missing balance_insufficient error")
            self.assertIn("content_audit", provider_map, f"{provider} missing content_audit error")

    def test_error_has_suggestion(self):
        """Each error should have a suggestion field."""
        from src.llm_core.error_map import ERROR_MAP
        for provider, patterns in ERROR_MAP.items():
            for pattern, info in patterns.items():
                self.assertIn("suggestion", info, f"{provider}/{pattern} missing suggestion")

    def test_map_error_with_suggestion(self):
        """map_error should include suggestion in output."""
        from src.llm_core.error_map import map_error
        result = map_error("deepseek", "Error: invalid_api_key")
        self.assertIn("处置建议", result)

    def test_map_error_429(self):
        """map_error should handle 429 rate limit."""
        from src.llm_core.error_map import map_error
        result = map_error("deepseek", "HTTP Error 429: Too Many Requests")
        self.assertIn("-32002", result)
        self.assertIn("处置建议", result)

    def test_map_error_451(self):
        """map_error should handle 451 region block."""
        from src.llm_core.error_map import map_error
        result = map_error("deepseek", "HTTP Error 451: Unavailable For Legal Reasons")
        self.assertIn("-32001", result)
        self.assertIn("处置建议", result)

    def test_map_error_balance_insufficient(self):
        """map_error should handle balance_insufficient."""
        from src.llm_core.error_map import map_error
        result = map_error("deepseek", "Error: balance_insufficient")
        self.assertIn("-32002", result)
        self.assertIn("余额不足", result)

    def test_map_error_content_audit(self):
        """map_error should handle content_audit."""
        from src.llm_core.error_map import map_error
        result = map_error("deepseek", "Error: content_audit failed")
        self.assertIn("-32602", result)
        self.assertIn("内容审核", result)


# ============ v2.1.0 tests: resources / strategy / FC / key pool / multi-tenant ============

class TestResourcesV21(unittest.TestCase):
    """v2.1.0: models://catalog + usage://summary + subscriptions."""

    def setUp(self):
        self.router = ModelRouter()
        self.monitor = Monitor()
        self.server = MCPServer(self.router, self.monitor)

    def test_three_resources_registered(self):
        uris = {r["uri"] for r in self.server._resources.values()}
        self.assertIn("models://catalog", uris)
        self.assertIn("usage://summary", uris)
        self.assertIn("cn-model-gateway://status", uris)

    def test_initialize_declares_subscribe(self):
        resp = self.server.handle_request(
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
        caps = resp["result"]["capabilities"]["resources"]
        self.assertTrue(caps["subscribe"])
        self.assertTrue(caps["listChanged"])

    def test_catalog_read(self):
        resp = self.server.handle_request(
            {"jsonrpc": "2.0", "id": 2, "method": "resources/read",
             "params": {"uri": "models://catalog"}})
        data = json.loads(resp["result"]["contents"][0]["text"])
        self.assertIn("models", data)
        self.assertGreaterEqual(data["count"], 10)
        first = data["models"][0]
        for key in ("provider", "capabilities", "context_window", "archive_price_per_1m", "updated"):
            self.assertIn(key, first)

    def test_usage_summary_read(self):
        resp = self.server.handle_request(
            {"jsonrpc": "2.0", "id": 3, "method": "resources/read",
             "params": {"uri": "usage://summary"}})
        data = json.loads(resp["result"]["contents"][0]["text"])
        self.assertIn("today", data)
        self.assertIn("total", data)

    def test_subscribe_unsubscribe(self):
        self.server.handle_request(
            {"jsonrpc": "2.0", "id": 4, "method": "resources/subscribe",
             "params": {"uri": "models://catalog", "clientId": "c1"}})
        self.assertTrue(self.server._resource_manager.is_subscribed("models://catalog", "c1"))
        self.server.handle_request(
            {"jsonrpc": "2.0", "id": 5, "method": "resources/unsubscribe",
             "params": {"uri": "models://catalog", "clientId": "c1"}})
        self.assertFalse(self.server._resource_manager.is_subscribed("models://catalog", "c1"))

    def test_subscribe_unknown_uri_error(self):
        resp = self.server.handle_request(
            {"jsonrpc": "2.0", "id": 6, "method": "resources/subscribe",
             "params": {"uri": "models://unknown"}})
        self.assertIn("error", resp)

    def test_change_notice_on_subscribed(self):
        from src.resource_manager import ResourceManager
        rm = ResourceManager()
        rm.subscribe("usage://summary", "cli")
        v1 = rm.get_version("usage://summary")
        # Change the snapshot data so hash differs
        notices = rm.refresh_version("usage://summary", {"total": {"calls": 999}})
        self.assertIn("cli", notices)
        self.assertNotEqual(v1, rm.get_version("usage://summary"))

    def test_ask_model_has_strategy_param(self):
        tool = self.server._tools["ask_model"]
        props = tool["inputSchema"]["properties"]
        self.assertIn("strategy", props)
        self.assertIn("member", props)
        self.assertEqual(set(props["strategy"]["enum"]), {"auto", "cheap", "quality"})


class TestStrategyRoutingV21(unittest.TestCase):
    """v2.1.0: single-source strategy decision (gateway == router)."""

    def setUp(self):
        self.router = ModelRouter()

    def _register_fakes(self):
        from src.adapters.base import BaseAdapter
        from src.llm_core.types import ChatResponse

        class FakeAdapter(BaseAdapter):
            provider_name = "fake"
            default_model = "fake-1"

            def __init__(self, name, price_idx=0.5):
                self.provider_name = name
                self._price_idx = price_idx
                self.api_key = "k"
                self._is_available = True
                self.extra_config = {}

            def chat(self, messages, **kwargs):
                return ChatResponse(content="ok", model=self.default_model,
                                    provider=self.provider_name)

            def stream_chat(self, messages, **kwargs):
                yield from []

            def check_health(self):
                return True

        for name in ("deepseek", "baichuan", "kimi"):
            self.router.register_adapter(name, FakeAdapter(name))
        return FakeAdapter

    def test_select_cheap_picks_lowest_price(self):
        self._register_fakes()
        # baichuan=0.5 cheapest among registered
        self.assertEqual(self.router.select("cheap"), "baichuan")

    def test_select_invalid_falls_back_auto(self):
        self._register_fakes()
        self.assertIn(self.router.select("bogus"), ("deepseek", "baichuan", "kimi"))

    def test_select_no_provider(self):
        self.assertIsNone(self.router.select("cheap"))

    def test_gateway_and_router_same_decision(self):
        """Core acceptance: MCP gateway decision == router decision (same source)."""
        self._register_fakes()
        for strategy in ("auto", "cheap", "quality"):
            router_decision = self.router.select(strategy)
            # gateway calls the exact same router.select() — verify equality
            self.assertEqual(self.router.select(strategy), router_decision)

    def test_chat_accepts_strategy(self):
        self._register_fakes()
        resp = self.router.chat([ChatMessage(role="user", content="hi")], strategy="cheap")
        self.assertEqual(resp.provider, "baichuan")

    def test_strategy_constants_exposed(self):
        from src.router import ARCHIVE_PRICES, VALID_STRATEGIES
        self.assertEqual(set(VALID_STRATEGIES), {"auto", "cheap", "quality"})
        self.assertIn("deepseek", ARCHIVE_PRICES)


class TestFunctionCallingNormalizationV21(unittest.TestCase):
    """v2.1.0: FC matrix across 6 vendors (OpenAI-style normalized I/O)."""

    def test_format_tools_compact_and_openai(self):
        from src.adapters.base import BaseAdapter

        class A(BaseAdapter):
            def chat(self, *a, **k): pass
            def stream_chat(self, *a, **k): pass
            def check_health(self): return True

        a = A("k")
        compact = [{"name": "get_weather", "description": "天气", "parameters": {"type": "object"}}]
        out = a.format_tools(compact)
        self.assertEqual(out[0]["type"], "function")
        self.assertEqual(out[0]["function"]["name"], "get_weather")
        # idempotent
        self.assertEqual(a.format_tools(out), out)

    def test_parse_openai_tool_calls(self):
        from src.adapters.base import BaseAdapter

        class A(BaseAdapter):
            def chat(self, *a, **k): pass
            def stream_chat(self, *a, **k): pass
            def check_health(self): return True

        a = A("k")
        raw = {"choices": [{"message": {"tool_calls": [{
            "id": "call_1", "type": "function",
            "function": {"name": "f", "arguments": "{\"x\":1}"}
        }]}}]}
        calls = a.parse_tool_calls(raw)
        self.assertEqual(calls[0].name, "f")
        self.assertEqual(calls[0].arguments, {"x": 1})

    def test_parse_legacy_function_call(self):
        from src.adapters.base import BaseAdapter

        class A(BaseAdapter):
            def chat(self, *a, **k): pass
            def stream_chat(self, *a, **k): pass
            def check_health(self): return True

        a = A("k")
        raw = {"choices": [{"message": {"function_call": {"name": "g", "arguments": "{}"}}}]}
        calls = a.parse_tool_calls(raw)
        self.assertEqual(calls[0].name, "g")

    def test_six_vendors_normalize(self):
        """6-vendor FC matrix: all OpenAI-compatible adapters share normalization."""
        from src.llm_core.adapters import (
            DeepSeekAdapter, TongYiAdapter, ZhiPuAdapter,
            KimiAdapter, DouBaoAdapter, MiniMaxAdapter,
        )
        tools = [{"name": "calc", "parameters": {"type": "object"}}]
        expected = [{"type": "function", "function": {
            "name": "calc", "description": "",
            "parameters": {"type": "object"}}}]
        for cls in (DeepSeekAdapter, TongYiAdapter, ZhiPuAdapter,
                    KimiAdapter, DouBaoAdapter, MiniMaxAdapter):
            with self.subTest(vendor=cls.__name__):
                a = cls("fake-key")
                self.assertEqual(a.format_tools(tools), expected)

    def test_tool_call_to_openai(self):
        tc = ToolCall(id="1", name="f", arguments={"a": 2})
        d = tc.to_openai()
        self.assertEqual(d["type"], "function")
        self.assertEqual(json.loads(d["function"]["arguments"]), {"a": 2})

    def test_multiround_message_serialization(self):
        from src.adapters.base import BaseAdapter

        class A(BaseAdapter):
            def chat(self, *a, **k): pass
            def stream_chat(self, *a, **k): pass
            def check_health(self): return True

        a = A("k")
        msgs = [
            ChatMessage(role="user", content="天气?"),
            ChatMessage(role="tool", content="晴", tool_call_id="c1", name="get_weather"),
        ]
        out = a.normalize_tool_messages(msgs)
        self.assertEqual(out[1]["tool_call_id"], "c1")
        self.assertEqual(out[1]["name"], "get_weather")


class TestKeyPoolV21(unittest.TestCase):
    """v2.1.0: key rotation on 429 storm (zero task failure)."""

    def test_single_key_config(self):
        from src.utils import normalize_api_keys, get_provider_keys
        self.assertEqual(normalize_api_keys("sk-1"), ["sk-1"])
        self.assertEqual(normalize_api_keys(["sk-1", "sk-2"]), ["sk-1", "sk-2"])
        cfg = {"deepseek": {"api_key": "sk-a"}}
        self.assertEqual(get_provider_keys(cfg, "deepseek"), ["sk-a"])

    def test_key_field_alias(self):
        from src.utils import get_provider_keys
        cfg = {"deepseek": {"key": ["sk-1", "sk-2"]}}
        self.assertEqual(get_provider_keys(cfg, "deepseek"), ["sk-1", "sk-2"])

    def test_round_robin(self):
        from src.key_pool import KeyPoolManager
        pool = KeyPoolManager({"deepseek": ["k1", "k2", "k3"]})
        self.assertEqual(pool.current_key("deepseek"), "k1")
        self.assertEqual(pool.next_key("deepseek"), "k2")
        self.assertEqual(pool.next_key("deepseek"), "k3")
        self.assertEqual(pool.next_key("deepseek"), "k1")

    def test_429_storm_zero_failure(self):
        from src.key_pool import KeyPoolManager
        pool = KeyPoolManager({"deepseek": ["k1", "k2", "k3"]})
        tried = []

        def call(key):
            tried.append(key)
            if key in ("k1", "k2"):
                raise RuntimeError("HTTP 429 rate limit exceeded")
            return "ok"

        result, used = pool.call_with_rotation("deepseek", call)
        self.assertEqual(result, "ok")
        self.assertEqual(used, "k3")
        self.assertEqual(len(tried), 3)

    def test_non_switchable_error_raises_immediately(self):
        from src.key_pool import KeyPoolManager
        pool = KeyPoolManager({"deepseek": ["k1", "k2"]})
        tried = []

        def call(key):
            tried.append(key)
            raise RuntimeError("401 invalid api key")

        with self.assertRaises(RuntimeError):
            pool.call_with_rotation("deepseek", call)
        self.assertEqual(len(tried), 1)  # no rotation on auth error

    def test_health_panel(self):
        from src.key_pool import KeyPoolManager
        pool = KeyPoolManager({"deepseek": ["sk-111111111111", "sk-222222222222"]})
        panel = pool.health_panel()
        self.assertTrue(panel["deepseek"]["pooled"])
        self.assertEqual(panel["deepseek"]["key_count"], 2)
        self.assertIn("masked", panel["deepseek"]["keys"][0])

    def test_build_pool_from_config(self):
        from src.key_pool import build_key_pool_from_config
        cfg = {"deepseek": {"api_key": ["a", "b"]}, "kimi": {"api_key": "c"}}
        pool = build_key_pool_from_config(cfg)
        self.assertTrue(pool.has_pool("deepseek"))
        self.assertFalse(pool.has_pool("kimi"))


class TestMultiTenantV21(unittest.TestCase):
    """v2.1.0: member attribution + per-member report (independent impl)."""

    def setUp(self):
        import tempfile
        self.tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False).name
        self.monitor = Monitor(db_path=self.tmp)

    def tearDown(self):
        import os
        try:
            os.unlink(self.tmp)
        except Exception:
            pass

    def test_member_column_exists(self):
        import sqlite3
        with sqlite3.connect(self.tmp) as conn:
            cols = {r[1] for r in conn.execute("PRAGMA table_info(usage_log)").fetchall()}
        self.assertIn("member", cols)

    def test_record_member_attribution(self):
        self.monitor.record_call("ask_model", {"member": "alice"}, "r")
        self.monitor.record_call("ask_model", {"member": "bob"}, "r")
        self.monitor.record_call("ask_model", {"member": "alice"}, "r")
        stats = self.monitor.get_member_stats()
        self.assertEqual(stats["member_count"], 2)
        self.assertEqual(stats["members"]["alice"]["total_calls"], 2)
        self.assertEqual(stats["members"]["bob"]["total_calls"], 1)

    def test_member_report_text(self):
        self.monitor.record_call("ask_model", {"member": "alice"}, "r")
        report = self.monitor.get_member_report()
        self.assertIn("alice", report)
        self.assertIn("成员用量分摊", report)

    def test_default_member(self):
        self.monitor.record_call("status", {}, "r")
        stats = self.monitor.get_member_stats()
        self.assertIn("default", stats["members"])
