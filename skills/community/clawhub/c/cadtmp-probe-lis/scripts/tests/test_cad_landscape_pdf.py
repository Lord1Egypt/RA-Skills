#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2]
SCRIPT = SKILL_DIR / "scripts" / "cad_landscape_pdf.py"


def fake_pdf_json() -> dict:
    return {
        "source_file": "/tmp/landscape_demo.pdf",
        "source_format": "pdf_vector",
        "pdf_meta": {
            "source_format": "pdf_vector",
            "pdf_type": "vector",
            "page_count": 3,
            "vector_text_count": 3,
            "vector_text_items": [
                {"page": 2, "text": "种植平面图 1:500", "x": 100, "y": 100, "width": 200, "height": 20},
                {"page": 3, "text": "国槐 胸径12cm", "x": 400, "y": 300, "width": 150, "height": 20},
                {"page": 3, "text": "紫薇 高度2m", "x": 400, "y": 500, "width": 120, "height": 20},
            ],
        },
        "contract": {"candidates": [], "review_candidates": []},
        "pdf_geometry_segments": [
            {"page": 2, "segments": [[10.0, 20.0, 30.0, 40.0], [30.0, 40.0, 50.0, 60.0]]},
        ],
    }


class LandscapePdfTest(unittest.TestCase):
    def test_pdf_json_text_classification(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            src = root / "pdf_fake.json"
            src.write_text(json.dumps(fake_pdf_json(), ensure_ascii=False), encoding="utf-8")
            out = root / "out"
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), str(src), "--out-dir", str(out)],
                capture_output=True, text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            out_json = out / "pdf_detail.landscape.json"
            self.assertTrue(out_json.exists(), proc.stdout + proc.stderr)
            payload = json.loads(out_json.read_text(encoding="utf-8"))
            self.assertEqual(payload.get("schema"), "cad-landscape-geometry/v1")
            self.assertGreaterEqual(payload["summary"]["plant_legends"], 1)
            self.assertEqual(payload["summary"]["green_area_candidates"], 0)
            self.assertEqual(payload["summary"]["paving_closed_areas"], 0)
            rows = {r.get("plant")[:4]: r for r in payload["plant_legends"]}
            self.assertTrue(any(k.startswith("国槐") for k in rows), rows.keys())
            guohuai = next(v for k, v in rows.items() if k.startswith("国槐"))
            self.assertEqual(guohuai["category"], "乔木")
            self.assertIn("missing_layer", guohuai.get("review_reasons", []))
            pdf_rows = payload.get("pdf_geometry_candidates") or []
            self.assertEqual(len(pdf_rows), 1)
            self.assertEqual(pdf_rows[0]["status"], "review")
            contract = payload["contract"]
            for item in contract["candidates"] + contract["review_candidates"]:
                self.assertIs(item["final_quantity"], False)


    def test_batch_two_json_inputs(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            a = root / "a.pdf识图.json"
            b = root / "b.pdf识图.json"
            payload = fake_pdf_json()
            a.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            b.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            out = root / "out"
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), str(a), str(b), "--out-dir", str(out)],
                capture_output=True, text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue((out / "a.pdf识图.landscape.json").exists(), proc.stdout)
            self.assertTrue((out / "b.pdf识图.landscape.json").exists(), proc.stdout)
            self.assertTrue((out / "_batch_summary.json").exists(), proc.stdout)

    def test_parse_page_list(self):
        import sys as _sys
        _sys.path.insert(0, str(SKILL_DIR / "scripts"))
        import cad_landscape_pdf as m
        self.assertEqual(m._parse_page_list("1,3-5"), [1, 3, 4, 5])
        self.assertEqual(m._parse_page_list("2"), [2])
        self.assertEqual(m._parse_page_list("0,3"), [3])
        self.assertIsNone(m._parse_page_list(""))
        self.assertIsNone(m._parse_page_list("x"))

    def test_pdfminer_vector_geometry_extraction(self):
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
        except Exception as exc:  # pragma: no cover
            self.skipTest(f"reportlab 不可用: {exc}")
        import sys as _sys
        _sys.path.insert(0, str(SKILL_DIR / "scripts"))
        from cad_pdf_geometry import extract_geometry_segments
        import tempfile, os
        with tempfile.TemporaryDirectory() as td:
            pdf = os.path.join(td, "geom_demo.pdf")
            c = canvas.Canvas(pdf, pagesize=A4)
            c.rect(50, 50, 150, 100, stroke=1, fill=0)
            c.line(250, 50, 320, 140)
            c.drawString(400, 400, "国槐 胸径12cm")
            c.save()
            res = extract_geometry_segments(pdf)
            self.assertTrue(res, res)
            total = sum(r["segment_count"] for r in res)
            self.assertGreaterEqual(total, 5, res)


if __name__ == "__main__":
    unittest.main()
