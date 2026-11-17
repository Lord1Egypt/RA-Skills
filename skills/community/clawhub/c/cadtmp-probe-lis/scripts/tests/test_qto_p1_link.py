# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from qto_project import QTO_SPEC, RECOG_DIR, build_project_yaml, init_project  # noqa: E402
from qto_p1_link import P1_GAP_KIND, P1_PENDING_KIND, run  # noqa: E402


def _write_recognition(root: Path, specialty: str, source_file: str = "sample.dxf"):
    d = root / RECOG_DIR / specialty
    d.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "cad-sample/v1",
        "source_file": source_file,
        "views": [
            {"id": "v1", "title": "一层平面图", "layer": "TITLE",
             "bbox": [0, 0, 10, 10], "confidence": 0.95, "status": "candidate"},
        ],
    }
    f = d / "recog-v1.json"
    f.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return f


class QtoP1LinkTest(unittest.TestCase):
    def test_single_specialty_writes_own_qty_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root, "示例工程", building="5#楼酒店",
                         recognized=["anzhuang-suanliang"])
            _write_recognition(root, "anzhuang-suanliang")
            res = run(root, "anzhuang-suanliang", when="20260101")
            self.assertTrue(res["ok"])
            self.assertIn("status", res)
            out = Path(res["out"])
            self.assertTrue(out.is_file())
            rel = out.relative_to(root).parts
            self.assertEqual(rel[0], "算量")
            self.assertEqual(rel[1], "anzhuang-suanliang")
            self.assertIn("anzhuang-suanliang__20260101.json", out.name)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["qto_spec"], QTO_SPEC)
            self.assertEqual(payload["specialty"], "anzhuang-suanliang")
            # 未给 --quantity：占位为 quantity_pending
            self.assertEqual(payload["placeholder"]["kind"], P1_PENDING_KIND)
            self.assertGreaterEqual(len(list((root / "算量").rglob("*.json"))), 1)

    def test_multi_specialty_writes_separate_dirs(self):
        specs = ["tujian-suanliang", "anzhuang-suanliang",
                 "zhuangshi-suanliang", "yuanlin-suanliang"]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root, "示例工程", source="explicit")
            for s in specs:
                _write_recognition(root, s, source_file=f"{s}.dwg")
            outs = []
            for s in specs:
                r = run(root, s, when="20260101")
                self.assertTrue(r["ok"], s)
                outs.append(Path(r["out"]))
            for s, o in zip(specs, outs):
                self.assertTrue(o.is_file())
                self.assertEqual(o.parent.name, s)
            # 四专业互不写对方目录
            for s in specs:
                others = [o for o in outs if o.parent.name != s]
                for oth in others:
                    self.assertNotIn(s, oth.name, oth.name)

    def test_missing_recognition_gap_is_nonblocking(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root, "示例工程", source="explicit")
            # 不写 识别/zhuangshi-suanliang/ 的 JSON
            (root / RECOG_DIR / "zhuangshi-suanliang").mkdir(parents=True, exist_ok=True)
            res = run(root, "zhuangshi-suanliang", when="20260101")
            self.assertTrue(res["ok"])  # 缺口不阻断体系
            self.assertEqual(res["status"], "gap")
            out = Path(res["out"])
            self.assertTrue(out.is_file())
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["placeholder"]["kind"], P1_GAP_KIND)

    def test_quantity_attach_marks_review_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root, "示例工程", building="5#楼酒店",
                         recognized=["yuanlin-suanliang"])
            _write_recognition(root, "yuanlin-suanliang")
            qty = root / "yuanlin-qty-temp.json"
            qty.write_text(json.dumps({
                "source_file": "yuanlin.dwg",
                "results": [{"item": "苗木", "count": 12}],
            }, ensure_ascii=False), encoding="utf-8")
            res = run(root, "yuanlin-suanliang", quantity=str(qty), when="20260101")
            self.assertEqual(res["status"], "ok")
            payload = json.loads(Path(res["out"]).read_text(encoding="utf-8"))
            self.assertIsNone(payload["placeholder"])
            cand = payload["contract"]["candidates"][0]
            self.assertFalse(cand["final_quantity"])
            self.assertIn("review", str(payload["project_key"]).lower())
            self.assertTrue(payload["project_key"]["review_required"])


if __name__ == "__main__":
    unittest.main()
