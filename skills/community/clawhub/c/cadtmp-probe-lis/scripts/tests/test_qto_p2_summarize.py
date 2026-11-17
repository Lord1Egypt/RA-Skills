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

from qto_project import init_project, write_project_yaml  # noqa: E402
from qto_p1_link import run as p1_run  # noqa: E402
from qto_p2_summarize import (  # noqa: E402
    STATUS_GAP,
    STATUS_MISSING,
    STATUS_NOT_INSTALLED,
    STATUS_OK,
    STATUS_PENDING,
    summarize_project,
    write_summary,
)


def _mk_recog(root: Path, slug: str, name: str = "酒店楼栋__%s__20260101.json"):
    d = root / "识别" / slug
    d.mkdir(parents=True, exist_ok=True)
    f = d / (name % slug)
    f.write_text(json.dumps({
        "schema": "cad-sample/v1", "source_file": f"{slug}.dwg",
        "views": [{"id": "v1", "title": "一层", "bbox": [0, 0, 1, 1], "confidence": 0.9, "status": "candidate"}],
    }, ensure_ascii=False), encoding="utf-8")
    return f


class QtoP2SummarizeTest(unittest.TestCase):
    def test_summary_statuses_and_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root, "示例工程", building="酒店楼栋", source="file",
                         recognized=["anzhuang-suanliang", "yuanlin-suanliang", "zhuangshi-suanliang"])
            # 基座识别（P2 不消费，但让项目结构完整）
            _mk_recog(root, "cad-file-reader")
            # ok：安装 有识别 + 附着既有量算
            _mk_recog(root, "anzhuang-suanliang")
            qty = root / "qty-anzhuang.json"
            qty.write_text(json.dumps({"source_file": "anzhuang.dwg", "results": [{"item": "管线", "n": 3}]},
                                      ensure_ascii=False), encoding="utf-8")
            p1_run(root, "anzhuang-suanliang", quantity=str(qty), when="20260101")
            # pending：园林 有识别但未给量
            _mk_recog(root, "yuanlin-suanliang")
            p1_run(root, "yuanlin-suanliang", when="20260101")
            # gap：装饰 缺识别
            p1_run(root, "zhuangshi-suanliang", when="20260101")
            # not_installed：土建未装，不写算量
            summary = summarize_project(root, when="20260101")
            got = {sp["specialty"]: sp["status"] for sp in summary["specialties"]}
            self.assertEqual(got["anzhuang-suanliang"], STATUS_OK)
            self.assertEqual(got["yuanlin-suanliang"], STATUS_PENDING)
            self.assertEqual(got["zhuangshi-suanliang"], STATUS_GAP)
            self.assertEqual(got["tujian-suanliang"], STATUS_NOT_INSTALLED)
            self.assertGreaterEqual(summary["totals"]["candidate_total"], 1)
            self.assertGreaterEqual(summary["totals"]["review_required_total"], 1)
            js, csvp = write_summary(root, summary)
            self.assertTrue(js.is_file())
            self.assertTrue(csvp.is_file())
            with csvp.open(encoding="utf-8-sig", newline="") as fh:
                rows = list(csv.DictReader(fh))
            self.assertTrue(any(r["状态"] == STATUS_GAP for r in rows))
            self.assertTrue(any(r["状态"] == STATUS_OK for r in rows))

    def test_no_qty_dir_marks_not_installed_or_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root, "示例项目", source="explicit")  # 四算量默认 not_installed
            summary = summarize_project(root, when="20260101")
            got = {sp["specialty"]: sp["status"] for sp in summary["specialties"]}
            for s in ("tujian-suanliang", "anzhuang-suanliang", "zhuangshi-suanliang", "yuanlin-suanliang"):
                self.assertEqual(got[s], STATUS_NOT_INSTALLED)


if __name__ == "__main__":
    unittest.main()
