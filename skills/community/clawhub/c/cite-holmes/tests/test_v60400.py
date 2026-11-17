#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v6.4.0 测试：测试线反馈五项（M1 TLS 降级重试/M2 OpenAlex 429 重试/
M3 arXiv 版本严格档/M5 元数据忠实度分级/M4 run_tests 入口）。

M1=TLS 指纹性超时（OpenSSL 3.0.13×Cloudflare TLS1.3 实测对 anthropic.com
必超时）→OP_NO_TLSv1_3 上下文重试一次；密封测试用宽松签名 mock（正式签名
(mock, timeout=None) 不接 context——TypeError 回退常规退避是设计行为）。
M5=fidelity 分级纯标签透出（判定语义零改动：partial 内 minor/major，
invalid 仍独占"完全编造"）。全部 sealed（mock/tmpdir，零网络）。"""
import json
import os
import ssl
import sys
import unittest
import unittest.mock

HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(SK, "scripts"))
import verify_refs as vr  # noqa: E402
from _mocks import fresh_engine_state  # noqa: E402


def _resp(payload):
    class _R:
        def read(self, n=-1):
            return json.dumps(payload).encode()

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False
    return _R()


class M1_TlsDowngrade(unittest.TestCase):
    def setUp(self):
        fresh_engine_state(vr)

    def test_tls_stall_triggers_tls12_context_retry(self):
        calls = []

        def loose_mock(req, timeout=None, context=None):
            calls.append("ctx" if context is not None else "plain")
            if context is None:
                raise ssl.SSLError("The handshake operation timed out")
            return _resp({"ok": 1})

        req = vr.urllib.request.Request("https://cdn.example.org/x")
        with unittest.mock.patch("urllib.request.urlopen",
                                 side_effect=loose_mock), \
             unittest.mock.patch.object(vr.time, "sleep", lambda s: None):
            with vr._urlopen_retry(req, 5) as r:
                assert json.loads(r.read())["ok"] == 1
        self.assertIn("ctx", calls, "TLS 特征异常未触发降级轮")
        self.assertEqual(calls[-1], "ctx", "降级轮应最后成功")

    def test_context_retry_only_once(self):
        calls = []

        def always_tls(req, timeout=None, context=None):
            calls.append("ctx" if context is not None else "plain")
            raise ssl.SSLError("handshake timed out")

        req = vr.urllib.request.Request("https://cdn.example.org/x")
        with unittest.mock.patch("urllib.request.urlopen",
                                 side_effect=always_tls), \
             unittest.mock.patch.object(vr.time, "sleep", lambda s: None):
            with self.assertRaises(ssl.SSLError):
                vr._urlopen_retry(req, 5)
        ctx_calls = [c for c in calls if c == "ctx"]
        self.assertEqual(len(ctx_calls), 1, "TLS1.2 降级只试一次")

    def test_non_tls_error_skips_downgrade(self):
        calls = []

        def plain_err(req, timeout=None, context=None):
            calls.append("ctx" if context is not None else "plain")
            raise vr.urllib.error.URLError("name resolution failed")

        req = vr.urllib.request.Request("https://api.example.org/x")
        with unittest.mock.patch("urllib.request.urlopen",
                                 side_effect=plain_err), \
             unittest.mock.patch.object(vr.time, "sleep", lambda s: None):
            with self.assertRaises(vr.urllib.error.URLError):
                vr._urlopen_retry(req, 5)
        self.assertNotIn("ctx", calls, "非 TLS 特征异常不应触发降级")

    def test_strict_mock_signature_falls_back(self):
        # 正式签名 mock（不接 context）→TypeError 回退常规退避（设计行为）
        calls = []

        def strict_mock(req, timeout=None):
            calls.append("call")
            if len(calls) == 1:
                raise ssl.SSLError("handshake timed out")
            return _resp({"ok": 1})

        req = vr.urllib.request.Request("https://cdn.example.org/x")
        with unittest.mock.patch("urllib.request.urlopen",
                                 side_effect=strict_mock), \
             unittest.mock.patch.object(vr.time, "sleep", lambda s: None):
            with vr._urlopen_retry(req, 5) as r:
                assert json.loads(r.read())["ok"] == 1
        self.assertGreaterEqual(len(calls), 2, "TypeError 应回退常规重试")


class M5_FidelityLabels(unittest.TestCase):
    def _match(self, sim_note):
        # 从 doi_metadata_match 的 note 生成路径测标签——直接调太重（需真网），
        # 这里锁三分支的源码标签存在性+阈值推导一致性
        src = open(os.path.join(SK, "scripts", "ch_registry.py"),
                   encoding="utf-8").read()
        self.assertIn("[元数据漂移:", src)
        self.assertIn('"minor" if sim >= 0.68 else "major"', src)
        self.assertEqual(src.count("[元数据漂移:"), 3,
                         "DOI 主分支+期刊作者分支+PMID 分支三处标签")

    def test_label_is_annotation_only(self):
        # 宪法锁（v6.6.0 F64 改 AST 形态——格式化器重排不再破锁）：携带
        # fidelity 标签的 return 元组，其首元素（判定域）只允许
        # "partial" 字面量 / jadj / aadj 变量 / 其 BoolOp 或 IfExp——
        # 绝不允许 invalid/空串；jadj/aadj 赋值处必须字面 "partial"。
        import ast
        src = open(os.path.join(SK, "scripts", "ch_registry.py"),
                   encoding="utf-8").read()
        self.assertIn('jadj = "partial"', src)
        self.assertIn('aadj = "partial"', src)
        tree = ast.parse(src)

        def _verdict_domain_ok(node):
            if isinstance(node, ast.Constant):
                return node.value == "partial"
            if isinstance(node, ast.Name):
                return node.id in ("jadj", "aadj")
            if isinstance(node, ast.BoolOp):
                return all(_verdict_domain_ok(v) for v in node.values)
            if isinstance(node, ast.IfExp):
                return (_verdict_domain_ok(node.body)
                        and _verdict_domain_ok(node.orelse))
            return False

        def _has_label(node):
            if isinstance(node, ast.Constant) and "元数据漂移:" in str(node.value):
                return True
            if isinstance(node, ast.JoinedStr):
                return any("元数据漂移:" in str(v.value or "")
                           for v in node.values if isinstance(v, ast.Constant))
            return False

        hits = 0
        for n in ast.walk(tree):
            if not (isinstance(n, ast.Return) and isinstance(n.value, ast.Tuple)):
                continue
            if not any(_has_label(e) for e in n.value.elts):
                continue
            hits += 1
            first = n.value.elts[0]
            self.assertTrue(_verdict_domain_ok(first),
                            f"标签 return 判定域越界: {ast.dump(first)[:80]}")
        self.assertEqual(hits, 3, "三处标签 return（DOI 主/期刊作者/PMID）")


class M2_OpenAlexRetry(unittest.TestCase):
    def test_helper_retries_429_once(self):
        calls = []

        def mock429(req, timeout=None):
            calls.append(req.full_url)
            if len(calls) == 1:
                raise vr.urllib.error.HTTPError(
                    req.full_url, 429, "rate limited",
                    {"Retry-After": "1"}, None)
            return _resp({"results": []})

        with unittest.mock.patch("urllib.request.urlopen",
                                 side_effect=mock429), \
             unittest.mock.patch.object(vr.time, "sleep", lambda s: None):
            out = vr._openalex_fetch("https://api.openalex.org/works?x", 5,
                                     "ua")
        self.assertEqual(len(calls), 2, "429 应重试一次")
        self.assertEqual(out, {"results": []})

    def test_helper_raises_on_persistent_429(self):
        calls = []

        def always429(req, timeout=None):
            calls.append(req.full_url)
            raise vr.urllib.error.HTTPError(req.full_url, 429, "rl",
                                            {}, None)

        with unittest.mock.patch("urllib.request.urlopen",
                                 side_effect=always429), \
             unittest.mock.patch.object(vr.time, "sleep", lambda s: None):
            with self.assertRaises(vr.urllib.error.HTTPError):
                vr._openalex_fetch("https://api.openalex.org/works?x", 5, "ua")
        self.assertEqual(len(calls), 2)


class M3_RequireVersion(unittest.TestCase):
    def test_flag_default_off_and_wiring(self):
        # 默认 off（_OPTS 无该键/False=零行为变化）+CLI 接线在场
        src = open(os.path.join(SK, "scripts", "ch_cli.py"),
                   encoding="utf-8").read()
        self.assertIn('"require_version": bool(args.require_version)', src)
        self.assertIn('"--require-version"', src)
        eng = open(os.path.join(SK, "scripts", "ch_registry.py"),
                   encoding="utf-8").read()
        self.assertIn('_ROOT._OPTS.get("require_version")', eng)
        # 封顶走 partial 通路且绝不 invalid
        seg = eng[eng.index('require_version"):'):]
        seg = seg[:seg.index("\n    if not title:")]
        self.assertIn('"partial"', seg)
        self.assertNotIn('"invalid"', seg)


class M4_RunTests(unittest.TestCase):
    def test_entry_ships_and_executable(self):
        p = os.path.join(SK, "tools", "run_tests.sh")
        self.assertTrue(os.path.isfile(p))
        self.assertTrue(os.access(p, os.X_OK))
        src = open(p, encoding="utf-8").read()
        self.assertIn("--verbose", src)   # 横向共性①：CI 里程碑
        self.assertIn("BUDGET", src)      # 耗时预算锁

    def test_whitelist_synced(self):
        t120 = open(os.path.join(HERE, "test_v120.py"),
                    encoding="utf-8").read()
        self.assertIn('"run_tests.sh"', t120)


if __name__ == "__main__":
    unittest.main()
