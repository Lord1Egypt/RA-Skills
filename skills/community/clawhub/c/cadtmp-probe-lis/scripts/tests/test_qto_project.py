# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from cad_contract import contractize_payload  # noqa: E402
from qto_project import (  # noqa: E402
    PLACEHOLDER_NOT_INSTALLED,
    RECOG_DIR,
    SKILL_SLUGS,
    build_project_yaml,
    default_project_key,
    dump_simple_yaml,
    init_project,
    load_simple_yaml,
    make_placeholder_payload,
    output_path,
    safe_name,
    wrap,
)
from qto_validate import validate_project  # noqa: E402


class QtoSafeTest(unittest.TestCase):
    def test_safe_name_strips_illegal_chars(self):
        self.assertEqual(safe_name("5#楼/酒店:一期"), "5#楼_酒店_一期")
        self.assertEqual(safe_name("  a  b  "), "a_b")

    def test_yaml_roundtrip(self):
        data = build_project_yaml("示例工程", source="explicit")
        parsed = load_simple_yaml(dump_simple_yaml(data))
        self.assertEqual(parsed["schema"], "qto-project/v1")
        self.assertEqual(parsed["project_key"]["project"], "示例工程")
        self.assertIn("tujian-suanliang", parsed["specialties"])


class QtoInitWrapTest(unittest.TestCase):
    def test_init_creates_layout_and_placeholder_valid(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            init_project(root, "示例工程", building="5#楼酒店", recognized=["tujian-suanliang"])
            self.assertTrue((root / ".qto/project.yaml").is_file())
            for slug in SKILL_SLUGS:
                self.assertTrue((root / RECOG_DIR / slug).is_dir())
            pkey = default_project_key("示例工程", "yuanlin-suanliang", building="5#楼酒店", source="file", review_required=True)
            payload = make_placeholder_payload("yuanlin-suanliang", pkey, "P1 未接入")
            out = output_path(root, "yuanlin-suanliang", pkey)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            report = validate_project(root)
            self.assertFalse(report["ok"])  # tujian active 但无文件 → fail；占位完整性单独验证见下

    def test_wrap_adds_qto_fields_and_keeps_v0(self):
        src = {
            "schema": "cad-sample/v1",
            "source_file": "sample.dxf",
            "views": [{"id": "v1", "title": "一层平面图", "layer": "TITLE", "bbox": [0, 0, 10, 10], "confidence": 0.95, "status": "candidate"}],
        }
        pkey = default_project_key("示例工程", "cad-file-reader", source="explicit")
        payload = wrap({"contract": contractize_payload(src)["contract"]}, "cad-file-reader", pkey)
        self.assertEqual(payload["qto_spec"], "qto-project/v1")
        self.assertEqual(payload["contract"]["schema"], "cad-file-reader/v0")
        self.assertEqual(payload["project_key"]["source"], "explicit")
        self.assertEqual(payload["draft_type"], "draft_type_pending")

    def test_validator_accepts_new_output_and_warns_legacy(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            init_project(root, "示例工程", source="explicit")
            pkey = default_project_key("示例工程", "cad-file-reader", source="explicit")
            payload = wrap({"contract": contractize_payload({
                "schema": "cad-sample/v1",
                "source_file": "sample.dxf",
                "views": [{"id": "v1", "title": "一层", "layer": "T", "bbox": [0, 0, 10, 10], "confidence": 0.95, "status": "candidate"}],
            })["contract"]}, "cad-file-reader", pkey)
            out = output_path(root, "cad-file-reader", pkey)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            # 其它四专业放占位
            for slug in ("tujian-suanliang", "anzhuang-suanliang", "zhuangshi-suanliang", "yuanlin-suanliang"):
                pp = default_project_key("示例工程", slug, source="file", review_required=True)
                po = output_path(root, slug, pp)
                po.parent.mkdir(parents=True, exist_ok=True)
                po.write_text(json.dumps(make_placeholder_payload(slug, pp, "占位"), ensure_ascii=False), encoding="utf-8")
            report = validate_project(root)
            self.assertTrue(report["ok"], report["errors"])
            self.assertGreaterEqual(report["placeholder_count"], 4)
            # 旧 v0 输出只 warning 不 fail
            legacy_path = root / RECOG_DIR / "cad-file-reader" / "legacy-old-v0.json"
            legacy_path.write_text(json.dumps({"contract": contractize_payload({
                "schema": "cad-other/v1", "source_file": "x.dwg",
                "views": [{"id": "v9", "title": "旧", "layer": "L", "bbox": [0, 0, 5, 5], "confidence": 0.5, "status": "review"}],
            })["contract"]}, ensure_ascii=False), encoding="utf-8")
            report2 = validate_project(root)
            self.assertTrue(report2["ok"], report2["errors"])  # 有效旧 v0 只识别不阻断
            legacy_files = [f for f in report2["files"] if Path(f["path"]).name == "legacy-old-v0.json"]
            self.assertTrue(legacy_files and legacy_files[0]["qto_spec"] is None)
            # 残缺旧 v0：只 warning 不 fail
            broken_legacy = root / RECOG_DIR / "cad-file-reader" / "legacy-broken-v0.json"
            broken_legacy.write_text(json.dumps({"contract": {"schema": "cad-file-reader/v0"}}, ensure_ascii=False), encoding="utf-8")
            report_legacy = validate_project(root)
            self.assertTrue(report_legacy["ok"], report_legacy["errors"])
            self.assertTrue(any("旧 v0 输出校验告警" in w for w in report_legacy["warnings"]))
            broken_legacy.unlink()
            # 新输出缺 qto_spec 字段会 fail：构造坏文件
            bad = dict(payload)
            bad.pop("project_key")
            bad_path = root / RECOG_DIR / "cad-file-reader" / "bad.json"
            bad_path.write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")
            report3 = validate_project(root)
            self.assertFalse(report3["ok"])

            # 占位完整性：登记 not_installed 但删除占位 → fail
            (root / RECOG_DIR / "tujian-suanliang" / (output_path(root, "tujian-suanliang",
                                default_project_key("示例工程", "tujian-suanliang", source="file"))).name).unlink()
            report4 = validate_project(root)
            self.assertFalse(report4["ok"])
            self.assertTrue(any("缺少占位" in str(e) for e in report4["errors"] + report4["warnings"]))


class QtoCliTest(unittest.TestCase):
    def test_qto_validate_cli_exit_code(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            init_project(root, "示例工程", building="5号楼")
            for slug in ("cad-file-reader", "tujian-suanliang", "anzhuang-suanliang", "zhuangshi-suanliang", "yuanlin-suanliang"):
                pp = default_project_key("示例工程", slug, building="5号楼",
                                         source="explicit" if slug == "cad-file-reader" else "file",
                                         review_required=(slug != "cad-file-reader"))
                if slug == "cad-file-reader":
                    payload = wrap({"contract": contractize_payload({
                        "schema": "cad-sample/v1", "source_file": "sample.dxf",
                        "views": [{"id": "v1", "title": "一层", "layer": "T", "bbox": [0, 0, 10, 10], "confidence": 0.95, "status": "candidate"}],
                    })["contract"]}, slug, pp)
                else:
                    payload = make_placeholder_payload(slug, pp, "占位")
                out = output_path(root, slug, pp)
                out.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(SKILL_DIR / "scripts" / "qto_validate.py"), str(root)],
                capture_output=True, text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            report = json.loads(proc.stdout)
            self.assertTrue(report["regression_pass"])
            self.assertGreaterEqual(report["placeholder_count"], 4)


if __name__ == "__main__":
    unittest.main()
