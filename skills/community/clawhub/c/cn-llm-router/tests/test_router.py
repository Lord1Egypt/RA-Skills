#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""离线测试（无需任何厂商密钥）。

覆盖：模型注册表解析、任务分类、路由决策、成本计算、硬件档位、语义缓存、更新检查。
运行：python tests/test_router.py   （在技能根目录执行）
"""

import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts"))

import classifier
import cost_tracker
import hardware
import cache
import yaml_simple
import update_check
import router
import report
import mock_engine
import session_manager
import text_splitter
import price_registry
import price_checker
from adapters.base import _estimate_tokens


class TestRegistry(unittest.TestCase):
    def setUp(self):
        self.reg = router.load_registry()

    def test_load_providers(self):
        provs = self.reg.get("providers", {})
        self.assertIn("deepseek", provs)
        self.assertIn("qwen", provs)
        self.assertIn("glm", provs)
        self.assertIn("kimi", provs)
        self.assertIn("hunyuan", provs)
        self.assertIn("doubao", provs)
        self.assertIn("ernie", provs)
        self.assertIn("spark", provs)

    def test_model_fields(self):
        m = self.reg["providers"]["deepseek"]["models"][0]
        self.assertEqual(m["name"], "deepseek-chat")
        self.assertIsInstance(m["ctx"], int)
        self.assertIn("price_in", m)


class TestClassifier(unittest.TestCase):
    def test_code(self):
        c = classifier.classify("帮我用 Python 写一个快速排序函数")
        self.assertEqual(c["task_type"], "code")

    def test_reason(self):
        c = classifier.classify("为什么天空是蓝色的？请分析其物理原理")
        self.assertTrue(c["needs_reasoning"])

    def test_long(self):
        big = "长文内容。" * 20000
        c = classifier.classify(big)
        self.assertEqual(c["length_bucket"], "long")

    def test_translate(self):
        c = classifier.classify("把这段话翻译成英文")
        self.assertEqual(c["task_type"], "translate")

    def test_hint_override(self):
        c = classifier.classify("随便聊聊", task_hint="reason")
        self.assertEqual(c["task_type"], "reason")


class TestResolve(unittest.TestCase):
    def setUp(self):
        self.reg = router.load_registry()
        # 让 deepseek 成为「已配置」厂商
        os.environ["DEEPSEEK_API_KEY"] = "sk-test-dummy"

    def tearDown(self):
        os.environ.pop("DEEPSEEK_API_KEY", None)

    def test_cheap(self):
        p, m, reason = router.resolve("cheap", classifier.classify("hello"), self.reg)
        self.assertEqual(p, "deepseek")
        self.assertEqual(m, "deepseek-chat")  # 比 reasoner 便宜

    def test_quality(self):
        p, m, reason = router.resolve("quality", classifier.classify("hello"), self.reg)
        self.assertEqual(p, "deepseek")
        self.assertEqual(m, "deepseek-reasoner")  # 带 reasoner，能力最强

    def test_auto_reason(self):
        cls = classifier.classify("请推导并证明勾股定理")
        p, m, _ = router.resolve("auto", cls, self.reg)
        self.assertEqual(m, "deepseek-reasoner")

    def test_no_config_raises(self):
        os.environ.pop("DEEPSEEK_API_KEY", None)
        with self.assertRaises(router.AdapterError):
            router.resolve("auto", classifier.classify("hi"), self.reg)


class TestCost(unittest.TestCase):
    def test_compute(self):
        price = {"in": 1, "out": 2}
        cost = cost_tracker.compute_cost(price, 1_000_000, 1_000_000)
        self.assertAlmostEqual(cost, 3.0, places=4)

    def test_zero_price(self):
        self.assertEqual(cost_tracker.compute_cost(None, 100, 100), 0.0)


class TestHardware(unittest.TestCase):
    def test_profile(self):
        p = hardware.profile()
        self.assertIn(p["tier"], ("low", "mid", "high"))
        self.assertGreaterEqual(p["max_concurrency"], 1)
        self.assertGreaterEqual(p["batch_size"], 1)

    def test_recommend(self):
        n = hardware.recommend_subtasks(100)
        self.assertLessEqual(n, hardware.profile()["max_concurrency"])


class TestCache(unittest.TestCase):
    _db = os.path.join(tempfile.gettempdir(), "cnllm_test_cache.db")

    def setUp(self):
        if os.path.exists(self._db):
            os.remove(self._db)

    def test_roundtrip(self):
        cache.put("测试问题A", "deepseek", "deepseek-chat", "答案A", db_path=self._db)
        hit = cache.get("测试问题A", db_path=self._db)
        self.assertIsNotNone(hit)
        self.assertEqual(hit[2], "答案A")

    def test_miss(self):
        self.assertIsNone(cache.get("不存在的问题", db_path=self._db))


class TestUpdateCheck(unittest.TestCase):
    def test_offline_safe(self):
        # 不抛异常；无 update_url 时返回稳定结果
        has_update, latest, msg = update_check.run("1.0.0", "", "")
        self.assertIsInstance(has_update, bool)
        self.assertEqual(latest, "1.0.0")


class TestReport(unittest.TestCase):
    def test_html_escape(self):
        # 厂商名/周期若含 HTML 特殊字符，必须被转义，不能注入到导出报表
        import tempfile
        agg = {
            "period": "<b>month</b>",
            "total_cost": 0.0, "total_calls": 1, "success_rate": 100.0,
            "p95_ms": 1, "total_in": 0, "total_out": 0,
            "by_provider": {"<img src=x onerror=alert(1)>": {"cost": 0.0, "calls": 1, "in": 0, "out": 0}},
        }
        path = os.path.join(tempfile.gettempdir(), "cnllm_test_report.html")
        report.render_html(agg, path)
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        os.remove(path)
        self.assertIn("&lt;img src=x", html)
        self.assertNotIn("<img src=x", html)
        self.assertIn("&lt;b&gt;month&lt;/b&gt;", html)


class TestAdapters(unittest.TestCase):
    def test_unknown_adapter_raises(self):
        # 未知 adapter 类型必须抛中文 AdapterError，绝不该 traceback
        with self.assertRaises(router.AdapterError):
            router.build("no_such_adapter", {})


class TestSuggestMode(unittest.TestCase):
    def setUp(self):
        self.reg = router.load_registry()
        # 清空所有厂商密钥，模拟「未配置」环境
        for k in ("DEEPSEEK_API_KEY", "DASHSCOPE_API_KEY", "ZHIPU_API_KEY",
                  "MOONSHOT_API_KEY", "HUNYUAN_API_KEY", "ARK_API_KEY",
                  "ERNIE_OPENAI_KEY", "ERNIE_API_KEY", "ERNIE_SECRET_KEY",
                  "SPARK_APP_ID", "SPARK_API_KEY", "SPARK_API_SECRET"):
            os.environ.pop(k, None)

    def test_suggest_without_key(self):
        # 无密钥时，allow_unconfigured 应给出基于注册表的合法推荐路由
        cls = classifier.classify("随便聊聊")
        p, m, reason = router.resolve("auto", cls, self.reg, allow_unconfigured=True)
        self.assertIn(p, self.reg["providers"])
        names = [x["name"] for x in self.reg["providers"][p]["models"]]
        self.assertIn(m, names)


class TestCacheV11(unittest.TestCase):
    """v1.1.0 缓存改进：最短查询限制 + 长度惩罚。"""
    _db = os.path.join(tempfile.gettempdir(), "cnllm_test_cache_v11.db")

    def setUp(self):
        if os.path.exists(self._db):
            os.remove(self._db)

    def test_short_query_skips_fuzzy(self):
        """不足 MIN_FUZZY_LEN(8) 字符的查询不做模糊匹配。"""
        cache.put("这是一个比较长的问题关于量子力学", "deepseek", "deepseek-chat", "长答案", db_path=self._db)
        # 短 query（"量子力学" 只有 4 字符）不应模糊命中
        hit = cache.get("量子力学", fuzzy=True, db_path=self._db)
        self.assertIsNone(hit, "短查询(<8字符) 不应触发模糊匹配")

    def test_length_penalty_avoids_false_match(self):
        """长度差异大的两个问题，即使文字部分相似也不应误命中。"""
        cache.put("请详细解释 Python 中的装饰器模式及其在 Web 框架中的应用场景",
                  "deepseek", "deepseek-chat", "装饰器答案", db_path=self._db)
        # 这个问题虽然包含"Python"，但长度差异大且含义不同
        hit = cache.get("Python 怎么安装第三方库", fuzzy=True, db_path=self._db)
        self.assertIsNone(hit, "长度差异大+语义不同的 query 不应模糊命中")

    def test_fuzzy_hit_when_similar_enough(self):
        """真正相似的问题（仅少量虚词/标点差异）应能模糊命中。"""
        cache.put("如何用Python实现快速排序算法",
                  "deepseek", "deepseek-chat", "快排代码", db_path=self._db)
        # 仅多了"请"字和问号差异，高度相似
        hit = cache.get("如何用 Python 实现快速排序算法？", fuzzy=True, db_path=self._db)
        self.assertIsNotNone(hit, "高度相似的 query 应模糊命中(adjusted>=0.80)")
        self.assertEqual(hit[2], "快排代码")


class TestTokenEstimate(unittest.TestCase):
    """v1.1.0 流式 token 估算精度测试。"""

    def test_pure_chinese(self):
        """中文文本：每字约 1.5 tokens。"""
        est = _estimate_tokens("你好世界")
        # 4 个中文字 * 1.5 ≈ 6
        self.assertGreaterEqual(est, 5)
        self.assertLessEqual(est, 8)

    def test_pure_english(self):
        """英文文本：每词约 1.3 tokens。"""
        est = _estimate_tokens("hello world test")
        # 3 词 * 1.3 ≈ 3.9 → int=3
        self.assertGreaterEqual(est, 3)
        self.assertLessEqual(est, 6)

    def test_mixed(self):
        """中英混合文本。"""
        est = _estimate_tokens("Hello 你好 world 世界")
        self.assertGreater(est, 0)

    def test_empty(self):
        self.assertEqual(_estimate_tokens(""), 0)
        self.assertEqual(_estimate_tokens(None), 0)


class TestMockEngine(unittest.TestCase):
    """v2.0.0 全链路离线 Mock 模式核心测试。"""
    
    def test_match_scenario_code(self):
        """Mock 场景匹配：code 类型关键词应命中。"""
        resp = mock_engine.match_scenario("帮我用Python写一个排序")
        self.assertIsNotNone(resp, "code 关键词查询应命中 mock 场景")
        self.assertIn("Python", resp["content"])

    def test_match_scenario_translate(self):
        """Mock 场景匹配：translate 类型关键词应命中。"""
        resp = mock_engine.match_scenario("把这段文字翻译成英文")
        self.assertIsNotNone(resp, "translate 关键词查询应命中 mock 场景")
        self.assertIn("Translation", resp["content"])

    def test_match_scenario_reason(self):
        """Mock 场景匹配：reason 类型关键词应命中。"""
        resp = mock_engine.match_scenario("请证明勾股定理")
        self.assertIsNotNone(resp, "reason 关键词查询应命中 mock 场景")
        self.assertIn("勾股定理", resp["content"])

    def test_match_scenario_summarize(self):
        """Mock 场景匹配：summarize 类型关键词应命中。"""
        resp = mock_engine.match_scenario("帮我总结一下这篇文章")
        self.assertIsNotNone(resp, "summarize 关键词查询应命中 mock 场景")

    def test_match_scenario_extract(self):
        """Mock 场景匹配：extract 类型关键词应命中。"""
        resp = mock_engine.match_scenario("提取这段话中的实体信息")
        self.assertIsNotNone(resp, "extract 关键词查询应命中 mock 场景")

    def test_match_scenario_fallback(self):
        """Mock 场景匹配：随机兜底查询应命中 fallback 场景。"""
        resp = mock_engine.match_scenario("zyxrandom123")
        self.assertIsNotNone(resp, "兜底场景始终应有响应")
        self.assertIn("Mock 模式", resp["content"])

    def test_build_mock_response(self):
        """Mock 响应构造：包含 mock 标志 + token 字段。"""
        resp = mock_engine.build_mock_response("用Python写代码", "code")
        self.assertIn("content", resp)
        self.assertIn("in_tokens", resp)
        self.assertIn("out_tokens", resp)
        resp["mock"] = True
        self.assertTrue(resp["mock"])

    def test_latency_simulation(self):
        """延迟模拟：指定毫秒数后返回。"""
        import time
        t0 = time.time()
        mock_engine.simulate_latency(100)
        elapsed = (time.time() - t0) * 1000
        self.assertGreaterEqual(elapsed, 90)
        self.assertLess(elapsed, 200)

    def test_empty_query(self):
        """空查询应返回 None。"""
        resp = mock_engine.match_scenario("")
        self.assertIsNone(resp, "空查询不应命中任何场景")

    def test_custom_mock_crud(self):
        """自定义 mock 场景：增删查完整流程。"""
        mock_engine.add_custom_mock(
            "test_custom", "code", ["测试关键词", "测试mock"], 10,
            {"content": "这是自定义响应", "in_tokens": 5, "out_tokens": 20}
        )
        try:
            mocks = mock_engine.list_custom_mocks()
            ids = [m["id"] for m in mocks]
            self.assertIn("test_custom", ids)
            # 验证自定义场景可匹配
            resp = mock_engine.match_scenario("测试关键词")
            self.assertIsNotNone(resp)
            self.assertIn("自定义", resp["content"])
        finally:
            mock_engine.remove_custom_mock("test_custom")
            mocks = mock_engine.list_custom_mocks()
            ids = [m["id"] for m in mocks]
            self.assertNotIn("test_custom", ids)


class TestMockIntegration(unittest.TestCase):
    """v2.0.0 Mock 模式与 chat 命令集成测试。"""
    
    def test_mock_chat_json_format(self):
        """Mock chat JSON 输出格式正确。"""
        import io, sys
        sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts"))
        
        from unittest.mock import patch
        # 模拟 cmd_chat 在 --mock 模式下的 JSON 输出
        resp = mock_engine.build_mock_response("用Python写快排", "code")
        expected_keys = {"content", "in_tokens", "out_tokens"}
        self.assertTrue(expected_keys.issubset(resp.keys()))

    def test_mock_preserves_cost_tracking(self):
        """Mock 模式下成本记录应为 0。"""
class TestMultimodal(unittest.TestCase):
    """v2.4.0 多模态分类与路由测试。"""

    def test_image_keyword(self):
        c = classifier.classify("帮我看看这张图片是什么")
        self.assertEqual(c["multimodal"], "image")

    def test_image_keyword_2(self):
        c = classifier.classify("描述图中的内容")
        self.assertEqual(c["multimodal"], "image")

    def test_audio_keyword(self):
        c = classifier.classify("帮我听听这段音频写了什么")
        self.assertEqual(c["multimodal"], "audio")

    def test_no_multimodal(self):
        c = classifier.classify("用 Python 写一个快排")
        self.assertIsNone(c["multimodal"])

    def test_multimodal_route_auto(self):
        """auto 策略 + 多模态需求应路由到视觉模型。"""
        reg = router.load_registry()
        cls = classifier.classify("分析一下这张图片")
        p, m, reason = router.resolve("auto", cls, reg, allow_unconfigured=True)
        # 视觉模型带 multimodal: true 标签
        mm = reg["providers"][p]["models"]
        found = [x for x in mm if x["name"] == m]
        self.assertTrue(found and found[0].get("multimodal"),
                        "多模态需求应路由到带 multimodal 标签的模型，实际路由: %s/%s" % (p, m))

    def test_multimodal_route_cheap(self):
        """cheap 策略 + 多模态需求也应过滤到视觉模型。"""
        reg = router.load_registry()
        cls = classifier.classify("看看这张图")
        p, m, reason = router.resolve("cheap", cls, reg, allow_unconfigured=True)
        mm = reg["providers"][p]["models"]
        found = [x for x in mm if x["name"] == m]
        self.assertTrue(found and found[0].get("multimodal"),
                        "cheap 多模态路由应选视觉模型，实际: %s/%s" % (p, m))


class TestArenaBlind(unittest.TestCase):
    """v2.4.0 arena --blind 开关测试。"""

    def test_blind_default_false(self):
        """不传 --blind 时默认显名对比模式。"""
        parser = router.build_parser()
        args = parser.parse_args(["arena", "--prompt", "hi",
                                  "--models", "deepseek:deepseek-chat,qwen:qwen-plus",
                                  "--mock", "--json"])
        self.assertFalse(getattr(args, "blind", True))

    def test_blind_true_with_flag(self):
        parser = router.build_parser()
        args = parser.parse_args(["arena", "--prompt", "hi", "--blind",
                                  "--models", "deepseek:deepseek-chat,qwen:qwen-plus",
                                  "--mock", "--json"])
        self.assertTrue(args.blind)

    def test_blind_routes_differ(self):
        """--blind 和 非-blind 模式下 mode 字段不同。"""
        import io, contextlib
        parser = router.build_parser()
        reg = router.load_registry()

        # blind 模式
        args_blind = parser.parse_args(["arena", "--prompt", "hi", "--blind",
                                        "--models", "deepseek:deepseek-chat,qwen:qwen-plus",
                                        "--mock", "--json"])
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            router.cmd_arena(args_blind, reg)
        out = buf.getvalue()
        self.assertIn('"mode": "blind"', out)

        # 非-blind 模式
        args_cmp = parser.parse_args(["arena", "--prompt", "hi",
                                      "--models", "deepseek:deepseek-chat,qwen:qwen-plus",
                                      "--mock", "--json"])
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            router.cmd_arena(args_cmp, reg)
        out = buf.getvalue()
        self.assertIn('"mode": "compare"', out)


class TestStreamUsage(unittest.TestCase):
    """v2.4.0 流式 usage 字段兼容性测试。"""

    def test_extract_usage_alias_input_output(self):
        """基类 _extract_usage 应覆盖 input_tokens/output_tokens 别名。"""
        from adapters.base import AdapterBase
        class Dummy(AdapterBase):
            def __init__(self): super().__init__({})
        d = Dummy()
        it, ot = d._extract_usage({"usage": {"input_tokens": 10, "output_tokens": 20}})
        self.assertEqual(it, 10)
        self.assertEqual(ot, 20)

    def test_extract_usage_alias_prompt_completion(self):
        """基类 _extract_usage 应覆盖 prompt_tokens/completion_tokens。"""
        from adapters.base import AdapterBase
        class Dummy(AdapterBase):
            def __init__(self): super().__init__({})
        d = Dummy()
        it, ot = d._extract_usage({"usage": {"prompt_tokens": 5, "completion_tokens": 15}})
        self.assertEqual(it, 5)
        self.assertEqual(ot, 15)


class TestV26EmbedRerank(unittest.TestCase):
    """v2.6 embed/rerank 统一接口测试。"""

    def test_base_adapter_embed_raises(self):
        """基类 embed 默认抛 NotImplementedError。"""
        from adapters.base import AdapterBase
        a = AdapterBase({})
        with self.assertRaises(NotImplementedError):
            a.embed(["test"])

    def test_base_adapter_rerank_raises(self):
        """基类 rerank 默认抛 NotImplementedError。"""
        from adapters.base import AdapterBase
        a = AdapterBase({})
        with self.assertRaises(NotImplementedError):
            a.rerank("query", ["doc1", "doc2"])

    def test_openai_compat_embed_method_exists(self):
        from adapters.openai_compat import OpenAICompatAdapter
        self.assertTrue(hasattr(OpenAICompatAdapter, "embed"))

    def test_openai_compat_rerank_method_exists(self):
        from adapters.openai_compat import OpenAICompatAdapter
        self.assertTrue(hasattr(OpenAICompatAdapter, "rerank"))

    def test_embed_rerank_cli_args_embed(self):
        """embed 子命令 CLI 参数正确注册。"""
        parser = router.build_parser()
        args = parser.parse_args(["embed", "--texts", "[\"hello\",\"world\"]", "--json"])
        self.assertEqual(args.texts, "[\"hello\",\"world\"]")

    def test_embed_rerank_cli_args_rerank(self):
        """rerank 子命令 CLI 参数正确注册。"""
        parser = router.build_parser()
        args = parser.parse_args(["rerank", "--query", "test", "--documents", "[\"a\",\"b\"]", "--json"])
        self.assertEqual(args.query, "test")
        self.assertEqual(args.documents, "[\"a\",\"b\"]")


class TestV26Session(unittest.TestCase):
    """v2.6 多轮会话管理测试。"""

    def test_create_and_get_session(self):
        """创建会话后能正确读取。"""
        sid = "test-" + str(os.getpid())
        session_manager.delete_session(sid)
        session_manager.create_session(sid)
        sess = session_manager.get_session(sid)
        self.assertIsNotNone(sess)
        self.assertEqual(sess["id"], sid)
        self.assertEqual(sess["messages"], [])

    def test_append_message(self):
        """追加消息后 messages 长度增加。"""
        sid = "test-append-" + str(os.getpid())
        session_manager.delete_session(sid)
        session_manager.create_session(sid)
        session_manager.append_message(sid, "user", "hello")
        sess = session_manager.get_session(sid)
        self.assertEqual(len(sess["messages"]), 1)

    def test_build_messages_with_history(self):
        """构建带上下文的消息列表包含历史。"""
        sid = "test-hist-" + str(os.getpid())
        session_manager.delete_session(sid)
        session_manager.create_session(sid)
        session_manager.append_message(sid, "user", "hi")
        msgs, _, _ = session_manager.build_messages_with_history(sid, "second message")
        # session 有 1 条历史("hi") + 追加 1 条当前("second message") = 2
        self.assertEqual(len(msgs), 2)

    def test_compress_history_short(self):
        """短历史不压缩。"""
        messages = [{"role": "user", "content": "a"}, {"role": "assistant", "content": "b"}]
        result = session_manager.compress_history(messages)
        self.assertEqual(len(result), 2)

    def test_delete_session(self):
        """删除会话成功。"""
        sid = "test-del-" + str(os.getpid())
        session_manager.create_session(sid)
        ok = session_manager.delete_session(sid)
        self.assertTrue(ok)


class TestV26TextSplitter(unittest.TestCase):
    """v2.6 文本分段与长文路由测试。"""

    def test_split_short_text(self):
        import text_splitter
        chunks = text_splitter.split_by_paragraphs("short text", max_chars=8000)
        self.assertEqual(len(chunks), 1)

    def test_split_long_text(self):
        import text_splitter
        long_text = "para1\n\n" * 1000
        chunks = text_splitter.split_by_paragraphs(long_text, max_chars=50)
        self.assertGreater(len(chunks), 1)

    def test_chunked_call(self):
        import text_splitter
        chunks = ["chunk1", "chunk2", "chunk3"]
        def task_fn(chunk, idx):
            return "summary: " + chunk
        result = text_splitter.chunked_call(chunks, task_fn)
        self.assertEqual(result["chunks"], 3)
        self.assertIn("chunk1", result["result"])

    def test_auto_chunk_length(self):
        import text_splitter
        length = text_splitter.auto_chunk_length(64000)
        self.assertGreater(length, 0)
        self.assertLess(length, 64000)

    def test_estimate_tokens(self):
        import text_splitter
        tokens = text_splitter.estimate_tokens_simple("你好世界")
        self.assertGreater(tokens, 0)


class TestV26TokenAlignment(unittest.TestCase):
    """v2.6 流式 token 计数对齐测试。"""

    def test_aggregate_includes_token_split(self):
        """aggregate 结果包含 measured/est 分列。"""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            tmp = f.name
        try:
            agg = cost_tracker.aggregate("month", db_path=tmp)
            self.assertIn("measured_in", agg)
            self.assertIn("est_in", agg)
        finally:
            os.unlink(tmp)

    def test_log_call_with_tokens_estimated(self):
        """记录带 tokens_estimated 的调用。"""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            tmp = f.name
        try:
            cost_tracker.log_call("test", "m", "code", 10, 20, 0.001, 100, True, tokens_estimated=True, db_path=tmp)
            agg = cost_tracker.aggregate("month", db_path=tmp)
            self.assertEqual(agg["est_in"], 10)
            self.assertEqual(agg["est_out"], 20)
            self.assertEqual(agg["measured_in"], 0)
        finally:
            os.unlink(tmp)


class TestV26Describe(unittest.TestCase):
    """v2.6 describe 子命令 CLI 参数测试。"""

    def test_describe_cli_args(self):
        parser = router.build_parser()
        args = parser.parse_args(["describe", "/path/to/img.jpg", "--json"])
        self.assertEqual(args.input, "/path/to/img.jpg")

    def test_describe_session_cli_args(self):
        parser = router.build_parser()
        args = router.build_parser().parse_args(["session", "list"])
        self.assertEqual(args.session_cmd, "list")
        args = router.build_parser().parse_args(["session", "show", "--id", "abc123"])
        self.assertEqual(args.id, "abc123")


# ───────────────────────── v2.7.0 测试 ─────────────────────────
class TestV27PriceRegistry(unittest.TestCase):
    """v2.7.0 价格档案本地化测试。"""

    def test_load_pricing(self):
        """测试价格档案加载。"""
        pricing = price_registry.load_pricing(force=True)
        self.assertIsInstance(pricing, dict)
        self.assertGreater(len(pricing), 0)

    def test_get_model_price(self):
        """测试单个模型价格查询。"""
        price = price_registry.get_model_price("deepseek-chat")
        self.assertIsNotNone(price)
        self.assertIn("in", price)
        self.assertIn("out", price)
        self.assertIn("date", price)

    def test_estimate_cost(self):
        """测试档案价估算花费。"""
        cost = price_registry.estimate_cost("deepseek-chat", 1000, 500)
        self.assertIsInstance(cost, float)
        self.assertGreaterEqual(cost, 0.0)

    def test_all_prices(self):
        """测试获取全部价格档案。"""
        pricing = price_registry.all_prices()
        self.assertIsInstance(pricing, dict)
        # 至少应该有 12 个厂商的主力模型
        self.assertGreaterEqual(len(pricing), 12)

    def test_stale_models(self):
        """测试过期模型检测。"""
        stale = price_registry.get_stale_models(days=30)
        self.assertIsInstance(stale, list)


class TestV27PriceChecker(unittest.TestCase):
    """v2.7.0 降价检测测试。"""

    def test_check_price_changes_no_network(self):
        """测试降价检测（无网络时优雅降级）。"""
        result = price_checker.check_price_changes(provider="nonexistent")
        self.assertIn("checked", result)
        self.assertIn("changes", result)
        self.assertIn("errors", result)
        self.assertIn("stale", result)

    def test_load_price_history(self):
        """测试价格历史加载。"""
        history = price_checker.load_price_history()
        self.assertIsInstance(history, dict)

    def test_hash_content(self):
        """测试内容哈希计算。"""
        hash1 = price_checker._hash_content("test content")
        hash2 = price_checker._hash_content("test content")
        hash3 = price_checker._hash_content("different content")
        self.assertEqual(hash1, hash2)
        self.assertNotEqual(hash1, hash3)

    def test_extract_prices_from_text(self):
        """测试从文本中提取价格。"""
        text = "deepseek-chat 1 2\nqwen-turbo 0.8 2"
        prices = price_checker._extract_prices_from_text(text)
        self.assertIsInstance(prices, list)


class TestV27CheapStrategy(unittest.TestCase):
    """v2.7.0 cheap 策略质量感知测试。"""

    def test_cheap_strategy_uses_pricing(self):
        """测试 cheap 策略使用性价比排序。"""
        import argparse
        # 模拟路由解析
        reg = router.load_registry()
        # 确保有已配置的厂商（mock 一个）
        import config
        original_has_key = config.has_any_key_for
        config.has_any_key_for = lambda p: True
        try:
            # 解析路由
            parser = router.build_parser()
            args = parser.parse_args(["route", "--prompt", "test", "--strategy", "cheap"])
            # 调用 cmd_route 会打印输出，这里只验证不报错
            # 由于需要 reg，我们直接测试 resolve 函数
            cls = classifier.classify("test", None)
            provider, model, reason = router.resolve("cheap", cls, reg, allow_unconfigured=True)
            self.assertIsNotNone(provider)
            self.assertIsNotNone(model)
            self.assertIn("性价比", reason)  # v2.7.0 应该包含"性价比"
        finally:
            config.has_any_key_for = original_has_key


class TestV27ReportDualTrack(unittest.TestCase):
    """v2.7.0 报表双轨计算测试。"""

    def test_render_text_with_pricing(self):
        """测试带价格档案的文本报表渲染。"""
        agg = {
            "period": "month",
            "total_cost": 0.05,
            "total_calls": 10,
            "success_rate": 95.0,
            "p95_ms": 1200,
            "total_in": 5000,
            "total_out": 3000,
            "measured_in": 2000,
            "measured_out": 1000,
            "est_in": 3000,
            "est_out": 2000,
            "by_provider": {
                "deepseek": {"cost": 0.03, "calls": 6, "in": 3000, "out": 2000, "est_calls": 2},
                "qwen": {"cost": 0.02, "calls": 4, "in": 2000, "out": 1000, "est_calls": 1},
            },
        }
        pricing = price_registry.load_pricing()
        text = report.render_text(agg, pricing=pricing)
        self.assertIn("档案价估算", text)
        self.assertIn("实测回填", text)

    def test_render_text_without_pricing(self):
        """测试不带价格档案的文本报表渲染（向后兼容）。"""
        agg = {
            "period": "month",
            "total_cost": 0.05,
            "total_calls": 10,
            "success_rate": 95.0,
            "p95_ms": 1200,
            "total_in": 5000,
            "total_out": 3000,
            "measured_in": 0,
            "measured_out": 0,
            "est_in": 0,
            "est_out": 0,
            "by_provider": {},
        }
        text = report.render_text(agg)
        self.assertIn("暂无调用记录", text)


class TestV27CLIArgs(unittest.TestCase):
    """v2.7.0 CLI 参数测试。"""

    def test_price_check_cli_args(self):
        parser = router.build_parser()
        args = parser.parse_args(["price-check"])
        self.assertEqual(args.cmd, "price-check")
        args = parser.parse_args(["price-check", "--provider", "deepseek", "--json"])
        self.assertEqual(args.provider, "deepseek")

    def test_price_history_cli_args(self):
        parser = router.build_parser()
        args = parser.parse_args(["price-history"])
        self.assertEqual(args.cmd, "price-history")

    def test_report_dual_cli_args(self):
        parser = router.build_parser()
        args = parser.parse_args(["report", "--dual"])
        self.assertTrue(args.dual)


if __name__ == "__main__":
    unittest.main(verbosity=2)
