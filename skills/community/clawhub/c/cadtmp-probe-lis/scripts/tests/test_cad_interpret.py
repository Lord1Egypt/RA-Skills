"""cad_interpret 规则解读与净跨覆盖测试（P0 补齐浅覆盖脚本）。"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2]
sys_path = SKILL_DIR / "scripts"
if str(sys_path) not in sys.path:
    sys.path.insert(0, str(sys_path))

import cad_interpret as it  # noqa: E402


class ExtractRefsTest(unittest.TestCase):
    def test_extract_standard_and_atlas(self):
        texts = [
            "执行 GB 50010-2010、16G101-1。",
            "另参见 04S519。",
            "JGJ/T 17-2008 作为补充。",
            "不认识的 YDB999 略过。",
        ]
        rows = it.extract_refs(texts)
        codes = {r["code"] for r in rows}
        self.assertIn("GB50010-2010", codes)
        self.assertIn("16G101-1", codes)
        self.assertIn("04S519", codes)
        self.assertIn("JGJ/T17-2008", codes)
        self.assertFalse(any(r["code"].startswith("YDB") for r in rows))

    def test_extract_refs_empty(self):
        self.assertEqual(it.extract_refs([]), [])


class ParseProfileTest(unittest.TestCase):
    def test_parse_concrete_cover_seismic_connection_lap(self):
        text = (
            "梁板柱混凝土等级C35，板保护层15mm，柱保护层20mm。"
            "抗震设防等级为三级。纵向钢筋连接采用机械连接，"
            "接头面积百分率不大于50%。"
        )
        p = it.parse_profile_text(text)
        self.assertEqual([c["value"] for c in p["concrete"]], ["C35"])
        self.assertEqual([c["value"] for c in p["cover"]], ["15", "20"])
        self.assertEqual([s["value"] for s in p["seismic"]], ["三级"])
        self.assertIn("机械连接", [c["value"] for c in p["connections"]])
        self.assertEqual([l["value"] for l in p["lap_percent"]], ["50%"])


class BeamRowsTest(unittest.TestCase):
    def test_user_net_span_override(self):
        data = {
            "members": {"梁": {"KL1": {"rawn": 1, "b": 300, "h": 700, "span": 2, "raws": ["KL1 300x700"]}}},
            "hits": [{"cat": "梁", "code": "KL1", "file": 0, "sheet": 1, "x": 0, "y": 0}],
            "geometry_segments": [],
        }
        rules, _ = it.load_rules(SKILL_DIR / "rules")
        profiles = it.collect_profiles(data.get("text_records") or [])
        rows = it.beam_rows(data, profiles, rules, {"net_spans_mm": "5000+4200"})
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["code"], "KL1")
        self.assertEqual(rows[0]["net_spans_mm"], [5000, 4200])
        self.assertEqual(rows[0]["span_status"], "用户覆盖净跨")


class BeamInstancesTest(unittest.TestCase):
    def test_beam_instances_split_by_sheet(self):
        data = {
            "files": [{"name": "结构图.dwg"}],
            "schema": "cad-scan-detail",
            "hits": [
                {"cat": "梁", "code": "KL1(2)", "raw": "KL1(2) 300x700", "file": 0, "sheet": 1, "x": 10, "y": 20},
                {"cat": "梁", "code": "KL1(2)", "raw": "KL1(2) C30", "file": 0, "sheet": 2, "x": 30, "y": 40},
            ],
            "layers": ["A"],
        }
        rows = it.beam_instances(data)
        self.assertEqual(len(rows), 2)
        self.assertEqual({r["sheet"] for r in rows}, {1, 2})
        self.assertTrue(all(r["code"] == "KL1(2)" for r in rows))
        # 实例不是最终算量：raw 只保留原文证据
        self.assertTrue(all("raw" in r for r in rows))


if __name__ == "__main__":
    unittest.main()


class SafeEvalExpressionTest(unittest.TestCase):
    """纯 AST 解释器：与原 eval 语义一致，且拒绝任意代码执行。"""

    def test_arithmetic_and_functions(self):
        self.assertEqual(it.safe_eval_expression("section_h_mm * 1.1 + max(2, 3) - min(1, 4)", {"section_h_mm": 300}), 332.0)
        self.assertEqual(it.safe_eval_expression("round(sqrt(900), 1)", {}), 30.0)
        self.assertEqual(it.safe_eval_expression("100 // 3 + 100 % 30", {}), 43)
        self.assertEqual(it.safe_eval_expression("-a + +b", {"a": 5, "b": 7}), 2)

    def test_compare_bool_ifexp(self):
        self.assertTrue(it.safe_eval_expression("section_h_mm >= 400 and section_h_mm < 600", {"section_h_mm": 450}))
        self.assertTrue(it.safe_eval_expression("1 < a <= 5", {"a": 3}))
        self.assertEqual(it.safe_eval_expression("a + 1 if a > 0 else -a", {"a": -5}), 5)
        self.assertEqual(it.safe_eval_expression("a or b", {"a": 0, "b": 7}), 7)

    def test_rejects_arbitrary_code(self):
        hostile = [
            "__import__('os').system('echo hi')",
            "().__class__.__base__.__subclasses__()",
            "open('/etc/passwd').read()",
            "[x for x in range(3)]",
            "sys.exc_info()",
            "namespace.get('_SAFE_FUNCS')",
            "a.b",
            "a[0]",
            "lambda: 1",
        ]
        for expr in hostile:
            with self.subTest(expr=expr):
                with self.assertRaises(ValueError):
                    it.safe_eval_expression(expr, {"sys": sys, "namespace": {}})

    def test_rejects_unknown_name(self):
        with self.assertRaises(ValueError):
            it.safe_eval_expression("unknown + 1", {})
