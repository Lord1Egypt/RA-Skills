# -*- coding: utf-8 -*-
from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from qto_project import init_project  # noqa: E402
from qto_p1_link import run as p1_run  # noqa: E402
from qto_p3_clash import clash_project, write_clash  # noqa: E402


def _mk_recog(root, slug, name="酒店楼栋__%s__20260101.json"):
    d = root / "识别" / slug
    d.mkdir(parents=True, exist_ok=True)
    f = d / (name % slug)
    f.write_text(json.dumps({
        "schema": "cad-sample/v1", "source_file": f"{slug}.dwg",
        "views": [{"id": "v1", "title": "一层", "bbox": [0, 0, 1, 1], "confidence": 0.9, "status": "candidate"}],
    }, ensure_ascii=False), encoding="utf-8")
    return f


class QtoP3ClashTest(unittest.TestCase):
    def test_multi_specialty_overlap_creates_cross_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            # 三个专业登记 active；同部位 酒店楼栋/一层 均在算量层登记
            init_project(root, "示例工程", building="酒店楼栋", source="file",
                         recognized=["tujian-suanliang", "anzhuang-suanliang", "zhuangshi-suanliang"])
            _mk_recog(root, "cad-file-reader")
            _mk_recog(root, "tujian-suanliang")
            _mk_recog(root, "anzhuang-suanliang")
            _mk_recog(root, "zhuangshi-suanliang")
            p1_run(root, "tujian-suanliang", when="20260101")
            p1_run(root, "anzhuang-suanliang", when="20260101")
            p1_run(root, "zhuangshi-suanliang", when="20260101")
            clash = clash_project(root, when="20260101")
            multi = [c for c in clash["cross_checks"] if c["specialty_count"] >= 2]
            self.assertGreaterEqual(len(multi), 1)
            self.assertGreaterEqual(clash["totals"]["multi_specialty_rooms"], 1)
            # 汇总层不生成最终量：totals.candidate_total 仍可能是 0（pending 登记）
            self.assertIn("candidate_total", clash["totals"])
            js, csvp = write_clash(root, clash)
            self.assertTrue(js.is_file())
            self.assertTrue(csvp.is_file())
            with csvp.open(encoding="utf-8-sig", newline="") as fh:
                rows = list(csv.DictReader(fh))
            self.assertGreaterEqual(len(rows), 3)

    def test_missing_and_gap_signals(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            # 只登记 zhuangshi 为 active，土建 not_installed
            init_project(root, "示例工程", source="file", recognized=["zhuangshi-suanliang"])
            _mk_recog(root, "cad-file-reader")
            _mk_recog(root, "zhuangshi-suanliang")
            p1_run(root, "zhuangshi-suanliang", when="20260101")
            clash = clash_project(root, when="20260101")
            got = {r["specialty"]: r["status"] for r in clash["specialties"]}
            self.assertEqual(got["zhuangshi-suanliang"], "pending" if got.get("zhuangshi-suanliang") else "gap")
            self.assertEqual(got["tujian-suanliang"], "not_installed")
            self.assertEqual(got["yuanlin-suanliang"], "not_installed")
            # 未安装专业不生成 missing
            self.assertNotIn("missing", clash["totals"]["status_counts"])


if __name__ == "__main__":
    unittest.main()
