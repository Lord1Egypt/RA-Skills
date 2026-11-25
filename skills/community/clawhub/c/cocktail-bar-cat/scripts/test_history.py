#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""历史查询与证据边界的标准库回归测试；不联网、不写业务数据。"""
import ast
import copy
import contextlib
import io
import json
import hashlib
import unittest
from unittest.mock import patch
import history


class HistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = history.load(history.ROOT / "cocktail_history.json")
        cls.recipes = history.load(history.ROOT / "recipes.json")["recipes"]

    def run_cli(self, args):
        output = io.StringIO()
        error = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            code = history.main(args)
        return code, output.getvalue(), error.getvalue()

    def test_structure(self):
        self.assertEqual(history.validate(self.data, self.recipes), [])

    def test_modern_recipe_count_unchanged(self):
        self.assertEqual(len(self.recipes), 177)
        fields = ("name", "name_en", "ingredients", "method", "glass", "garnish")
        specs = [{k: ([{key: value for key, value in i.items() if key != "brand"}
                       for i in r[k]] if k == "ingredients" else r.get(k))
                  for k in fields} for r in self.recipes]
        digest = hashlib.sha256(json.dumps(specs, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
        # v2.7.3专用版规格基线；相对v2.7.2唯一method差异为第175条不点火安全改编。
        # 其余177款材料/用量/杯具/装饰与合成金额不变，演示金额另在test_public.py校验。
        self.assertEqual(digest, "285af2c735adc8cbc2bc8a01d864a3e4caafdb3613a81c50f7a21fa25521e6e6")

    def test_exact_english_and_standard_name(self):
        for r in self.data["records"]:
            found = history.select(self.data, self.recipes, r["name_en"])
            self.assertIn(r["id"], [x["id"] for x in found])
            if r.get("canonical_name"):
                found = history.select(self.data, self.recipes, r["canonical_name"])
                self.assertIn(r["id"], [x["id"] for x in found])

    def test_all_registered_aliases(self):
        for r in self.data["records"]:
            for alias in r.get("aliases", []):
                self.assertIn(r["id"], [x["id"] for x in history.select(self.data, self.recipes, alias)])

    def test_family_filter(self):
        self.assertEqual(len(self.data["families"]), 6)
        self.assertTrue(history.select(self.data, self.recipes, family="sour"))
        self.assertTrue(all(x["family_id"] == "sour" for x in history.select(self.data, self.recipes, family="sour")))

    def test_unknown_explicit_not_invented(self):
        code, out, _ = self.run_cli(["不存在的虚构酒ABC", "--json"])
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(out)["records"], [])
        self.assertIn("未收录", json.loads(out)["note"])

    def test_missing_data_fails_closed(self):
        with patch.object(history, "load", side_effect=FileNotFoundError("missing")):
            code, _, error = self.run_cli(["古典"])
        self.assertEqual(code, 2)
        self.assertIn("不要退回旧故事断言", error)

    def test_compare_and_creative_are_separate(self):
        r = next(x for x in self.data["records"] if x.get("historical_versions") and x.get("canonical_name"))
        code, out, _ = self.run_cli([r["id"], "--compare", "--creative"])
        self.assertEqual(code, 0)
        self.assertIn("原书", out)
        self.assertIn("不是原书换算", out)
        self.assertIn("未经实饮验证", out)
        self.assertIn("只动", out)

    def test_invalid_reference_detected(self):
        bad = copy.deepcopy(self.data)
        bad["records"][0]["claims"][0]["source_ids"] = ["nonexistent"]
        self.assertTrue(history.validate(bad, self.recipes))

    def test_secondary_cannot_pose_as_primary(self):
        bad = copy.deepcopy(self.data)
        for source in bad["sources"]:
            source["kind"] = "secondary"
        self.assertTrue(any("documented" in x for x in history.validate(bad, self.recipes)))

    def test_duplicate_and_expression_evidence_detected(self):
        bad = copy.deepcopy(self.data)
        bad["sources"].append(copy.deepcopy(bad["sources"][0]))
        self.assertTrue(history.validate(bad, self.recipes))
        bad = copy.deepcopy(self.data)
        bad["records"][0]["claims"][0].pop("evidence_record", None)
        self.assertTrue(any("独立事实摘要" in x for x in history.validate(bad, self.recipes)))
        injected = copy.deepcopy(self.data)
        injected["records"][0]["claims"][0]["quote_en"] = "third party wording"
        self.assertTrue(any("MIT-0版仍随包保存" in x for x in history.validate(injected, self.recipes)))

    def test_edition_mismatch_detected(self):
        bad = copy.deepcopy(self.data)
        sources = {s["id"]: s for s in bad["sources"]}
        version = next(v for r in bad["records"] for v in r.get("historical_versions", []) if sources[v["source_id"]]["kind"] == "primary_transcription")
        version["year"] = 9999
        self.assertTrue(any("年份" in x for x in history.validate(bad, self.recipes)))

    def test_invalid_data_cannot_bypass_validation(self):
        bad = copy.deepcopy(self.data)
        bad["records"][0]["claims"][0]["source_ids"] = ["missing-source"]
        with patch.object(history, "load", side_effect=[bad, {"recipes": self.recipes}]):
            code, out, error = self.run_cli([bad["records"][0]["id"]])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("停止事实输出", error)

    def test_catalog_cannot_support_recipe_or_secondary_claim(self):
        bad = copy.deepcopy(self.data)
        sid = bad["records"][0]["claims"][0]["source_ids"][0]
        src = next(s for s in bad["sources"] if s["id"] == sid)
        src["kind"] = "catalog_only"
        src["verification"] = "catalog_checked"
        c = bad["records"][0]["claims"][0]
        c["status"] = "supported_secondary"
        c["source_ids"] = [sid]
        self.assertTrue(any("二手事实" in x for x in history.validate(bad, self.recipes)))

    def test_compare_text_includes_every_version_source(self):
        for r in self.data["records"]:
            if not r.get("historical_versions"):
                continue
            code, out, _ = self.run_cli([r["id"], "--compare"])
            self.assertEqual(code, 0)
            sources = {s["id"]: s for s in self.data["sources"]}
            for v in r["historical_versions"]:
                self.assertIn(sources[v["source_id"]]["url"], out)
                self.assertIn(sources[v["source_id"]]["edition"], out)

    def test_creative_is_not_historical(self):
        self.assertTrue(all(r["creative_bridge"]["not_historical"] is True for r in self.data["records"]))
        self.assertTrue(all(isinstance(r["creative_bridge"]["changed_variable"], str) for r in self.data["records"]))
        code, out, _ = self.run_cli(["--menu", "--json"])
        self.assertEqual(code, 0)
        self.assertGreaterEqual(len(json.loads(out)["menu_frameworks"]), 3)

    def test_historical_sources_do_not_expire(self):
        self.assertTrue(self.data["policy"]["historical_sources_do_not_expire"])
        before = copy.deepcopy(self.data)
        history.select(self.data, self.recipes)
        self.assertEqual(before, self.data)
        code, out, _ = self.run_cli(["--stats", "--json"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["records"], len(self.data["records"]))

    def test_script_no_network_or_business_writes(self):
        tree = ast.parse((history.ROOT / "scripts/history.py").read_text(encoding="utf-8"))
        modules = {n.name.split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.Import) for n in node.names}
        self.assertFalse(modules & {"requests", "urllib", "socket", "httpx", "aiohttp"})
        attrs = {node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)}
        self.assertFalse(attrs & {"write_text", "write_bytes", "unlink", "rename", "mkdir"})

    def test_story_history_links_and_safety(self):
        stories = history.load(history.ROOT / "cocktail_stories.json")["stories"]
        ids = {r["id"] for r in self.data["records"]}
        for s in stories:
            self.assertTrue(all(rid in ids for rid in s.get("history_record_ids", [])))
            self.assertEqual(s.get("quote_type"), "original_bar_copy_not_historical_quote")
            self.assertTrue(s.get("history_status"))
        b52 = next(s for s in stories if s["name_en"] == "B-52")
        self.assertNotIn("吸完", b52.get("serving_tip", ""))
        self.assertIn("不点火", b52.get("serving_tip", ""))


if __name__ == "__main__":
    unittest.main(verbosity=2)
