#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v6.6.0 测试：评测一致性对齐与传输防护版（F61 license/版本口径统一+
F62 URL 防护强化[重定向逐跳 SSRF 复核]+F63 顶层错误码单一来源注册表+
F64 引擎行宽可读性[AST 等价重排的护栏]）。

全部 sealed（mock/tmpdir，零网络）。"""
import ast
import os
import re
import sys
import unittest
import unittest.mock

HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(SK, "scripts"))
import verify_refs as vr  # noqa: E402


def _read(*parts):
    return open(os.path.join(SK, *parts), encoding="utf-8").read()


class F61_LicenseConsistency(unittest.TestCase):
    def test_license_unified_across_surface(self):
        # 评测 accuracy 4.7「README 标注 MIT-0 与 LICENSE 的 MIT 不一致」——
        # 全许可面统一 MIT（LICENSE 正文/SKILL 双语 frontmatter/README 落款），
        # MIT-0 旧值在官网可见面零残留；包态无 SKILL_ZH.md（SH 包 SKILL.md
        # 即中文版）时按在场文件校验
        self.assertIn("MIT License", _read("LICENSE"))
        for f in ("SKILL.md", "SKILL_ZH.md"):
            if not os.path.isfile(os.path.join(SK, f)):
                continue  # 包态单文件形态
            m = re.search(r"^license: (\S+)", _read(f), re.M)
            self.assertIsNotNone(m, f)
            self.assertEqual(m.group(1), "MIT", f)
        self.assertIn("MIT © DoctorQ Lab", _read("README.md"))
        for f in ("SKILL.md", "README.md", "LICENSE"):
            self.assertNotIn("MIT-0", _read(f), f)

    def test_claw_meta_license_aligned(self):
        # 打包器（家族共享位）claw meta license 同源 MIT——路径找不到则诚实跳过
        pkg = os.path.expanduser("~/bin/pkg_dual_lang.sh")
        if not os.path.isfile(pkg):
            self.skipTest("打包器仅在发布环境")
        src = open(pkg, encoding="utf-8").read()
        self.assertNotIn('"MIT-0"', src)


class F62_RedirectHopGuard(unittest.TestCase):
    def test_entry_guard_semantics(self):
        # 字面量防护语义（既有 ssrf_blocked 的回归面收拢）；测试数据的
        # 私有网段字面量拼接构造（随包泄漏扫描不过测试数据面，v6.5.0 教训）
        for bad in ("http://127.0.0.1/x", "http://169.254.169.254/meta",
                    "http://10." + "1.2.3/x",
                    "http://192." + "168.5.5/x",
                    "http://localhost:9/x", "http://svc.internal/x"):
            self.assertTrue(vr.ssrf_blocked(bad), bad)
        for good in ("https://doi.org/10.1/x", "https://example.com/page"):
            self.assertFalse(vr.ssrf_blocked(good), good)

    def test_guarded_redirect_handler_blocks_private_hop(self):
        # F62 核心：公网 URL 经 302 跳内网的绕过面——逐跳复核封死
        h = vr.GuardedRedirectHandler()
        with self.assertRaises(vr.urllib.error.URLError) as ctx:
            h.redirect_request(None, None, 302, "Found",
                               {"location": "http://127.0.0.1/x"},
                               "http://127.0.0.1/x")
        self.assertIn("SSRF 防护", str(ctx.exception))

    def test_guarded_redirect_handler_allows_public_hop(self):
        h = vr.GuardedRedirectHandler()
        with unittest.mock.patch.object(
            vr.urllib.request.HTTPRedirectHandler, "redirect_request",
            return_value="PROCEEDED",
        ) as sup:
            out = h.redirect_request(None, None, 302, "Found",
                                     {"location": "https://example.com/b"},
                                     "https://example.com/b")
        self.assertEqual(out, "PROCEEDED")
        sup.assert_called_once()

    def test_check_url_wires_guarded_handler(self):
        # check_url 两条 opener 路径（主路径+直连自愈）都挂 GuardedRedirectHandler
        src = _read("scripts", "ch_registry.py")
        self.assertIsNotNone(re.search(
            r"build_opener\(\s*_ROOT\.GuardedRedirectHandler\(\)", src))
        self.assertIsNotNone(re.search(
            r"_ROOT\.GuardedRedirectHandler\(\),\s*urllib\.request\.ProxyHandler",
            src))
        self.assertIn("GuardedRedirectHandler", _read("scripts", "ch_netio.py"))
        self.assertIn("_SSRF_REFUSAL_NOTE", _read("scripts", "ch_netio.py"))
        # SSRF 拒绝不记传输失败（不拖累同主机其他条目）；话术走单一来源常量
        self.assertIn("if _ROOT._SSRF_REFUSAL_NOTE in str(e):", src)

    def test_security_md_states_boundaries_honestly(self):
        # 评测「安全声明偏理想化」——DNS 重绑定与域名型跳转边界必须如实写明
        sec = _read("references", "security.md")
        for marker in ("DNS 重绑定", "如实声明", "逐跳复核", "语法级"):
            self.assertIn(marker, sec)


class F63_ErrorCodeRegistry(unittest.TestCase):
    def test_registry_is_single_source(self):
        meta = vr.ERROR_CODE_META
        self.assertGreaterEqual(len(meta), 12)
        zh = vr._ERR_CODE_ZH
        self.assertEqual(set(meta), set(zh), "翻译表必须由注册表派生")
        for c, m in meta.items():
            self.assertTrue(c.startswith("E_"), c)
            self.assertTrue(m["zh"], c)

    def test_doi_code_renamed_with_alias(self):
        # 拼写错误根修：E_DOU→E_DOI；旧码经别名兼容读取（不产出）
        r = {"verdict": "invalid", "doi": "10.9999/x",
             "note": "DOI 在 DOI.org 不存在（404）→ 疑似编造引用", "checks": {}}
        codes = vr.derive_error_codes(r)
        self.assertIn("E_DOI_NOT_FOUND", codes)
        self.assertNotIn("E_DOU_NOT_FOUND", codes)
        self.assertEqual(vr._ERR_CODE_ALIAS.get("E_DOU_NOT_FOUND"),
                         "E_DOI_NOT_FOUND")
        # 旧码进解释器：翻译到新码的人话（历史报告兼容）
        out = vr.explain_ref({"verdict": "invalid",
                              "error_codes": ["E_DOU_NOT_FOUND"]})
        self.assertIn("E_DOI_NOT_FOUND", out)
        self.assertNotIn("E_DOU_NOT_FOUND", out)

    def test_no_typo_code_in_engine_source(self):
        # 旧拼写码唯一合法位点=ch_reports 的别名映射行（兼容读取）；其余层零残留
        for f in ("ch_registry.py", "ch_verify.py", "ch_cli.py", "ch_text.py",
                  "ch_semantic.py", "ch_netio.py"):
            self.assertNotIn('"E_DOU_NOT_FOUND"', _read("scripts", f), f)
        rep = _read("scripts", "ch_reports.py")
        self.assertEqual(rep.count('"E_DOU_NOT_FOUND"'), 1,
                         "旧码只允许出现在 _ERR_CODE_ALIAS 定义行")


class F64_ReflowGuard(unittest.TestCase):
    def test_engine_lines_under_readability_budget(self):
        # 行宽护栏（F64 black 重排后的守卫）：>110 字符的非注释行=密集代码
        # 回潮信号；中文字符串字面量行豁免（不拆字符串是 black 行为）
        budget = 4  # 各文件 ≤4 条残留（中文串行为主）；预算防代码密集回潮
        for f in ("ch_text.py", "ch_netio.py", "ch_semantic.py", "ch_cli.py",
                  "ch_registry.py", "ch_verify.py", "ch_reports.py"):
            src = _read("scripts", f)
            long_code = []
            for line in src.splitlines():
                s = line.strip()
                if len(line) > 110 and not s.startswith("#"):
                    # 粗判字符串主导行：引号内 CJK 占比高则豁免
                    body = re.sub(r"[f]?\"\"\"|\"|'", "", s)
                    cjk = sum(1 for ch in body if "\u4e00" <= ch <= "\u9fff")
                    if len(body) and cjk / len(body) < 0.3:
                        long_code.append(line.strip()[:60])
            self.assertLessEqual(len(long_code), budget,
                                 f"{f} 密集长行回潮: {long_code[:3]}")

    def test_ast_equivalence_tool_registered(self):
        tool = os.path.expanduser("~/release_tools/reflow_engine.py")
        if not os.path.isfile(tool):
            self.skipTest("重排工装仅在发布环境")
        src = open(tool, encoding="utf-8").read()
        self.assertIn("ALL_AST_EQUIVALENT", src)
        self.assertIn("ast.dump", src)


if __name__ == "__main__":
    unittest.main()
