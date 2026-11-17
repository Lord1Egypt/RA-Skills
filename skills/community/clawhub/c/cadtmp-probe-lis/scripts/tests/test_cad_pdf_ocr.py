import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "cad_pdf_ocr.py"
VALIDATE = ROOT / "scripts" / "cad_validate.py"
import sys
from pathlib import Path as _P
sys.path.insert(0, str(ROOT / "scripts"))
from cad_pdf_ocr import _review_image_name, build_contract  # noqa: E402
from cad_contract import validate_contract_payload  # noqa: E402




class CadPdfOcrTest(unittest.TestCase):
    def _make_text_pdf(self, workdir: Path, name: str = "sample") -> Path:
        if shutil.which("soffice") is None:
            self.skipTest("soffice 不可用，跳过 PDF 生成用例")
        txt = workdir / f"{name}.txt"
        txt.write_text("一层平面图\nC30 混凝土\n消防栓 2531\n项目名称：测试工程\n图号：JD-01\n比例：1:100\n", encoding="utf-8")
        pdf = workdir / f"{name}.pdf"
        subprocess.run(
            ["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(workdir), str(txt)],
            check=True, capture_output=True, timeout=120,
        )
        return pdf

    def test_text_pdf_contract_review_and_meta(self):
        with tempfile.TemporaryDirectory(prefix="cad-pdfocr-test-") as tmp:
            workdir = Path(tmp)
            pdf = self._make_text_pdf(workdir)
            out = workdir / "out"
            proc = subprocess.run(
                ["python3", str(SCRIPT), str(pdf), "--out-dir", str(out), "--workers", "2"],
                capture_output=True, text=True, timeout=300,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            report = json.loads(proc.stdout)
            result = report["results"][0]
            self.assertIsNone(result["error"])
            self.assertIn(result["pdf_type"], ("text_based", "mixed", "scanned"))
            self.assertIn(result["source_format"], ("pdf_vector", "pdf_raster", "pdf_hybrid"))

            out_json = out / f"{pdf.stem}.pdf识图.json"
            self.assertTrue(out_json.exists())
            payload = json.loads(out_json.read_text(encoding="utf-8"))
            self.assertEqual(payload["contract"]["schema"], "cad-file-reader/v0")
            self.assertEqual(payload["contract"]["summary"]["total"], payload["contract"]["summary"]["review_required"])
            self.assertIn(payload["source_format"], ("pdf_vector", "pdf_raster", "pdf_hybrid"))
            # 候选必须带 page_index / page_bbox / source_format
            for cand in payload["contract"]["review_candidates"]:
                self.assertFalse(cand["final_quantity"])
                self.assertEqual(cand["confidence_tier"], "review_required")
                self.assertIn("missing_layer", cand["review_reasons"])
                self.assertIn("page_index", cand)
                self.assertIn("page_bbox", cand)
                self.assertIn("source_format", cand)
                self.assertEqual(cand["source_format"], payload["source_format"])
            # 图签栏字段（项目名称/图号/比例）应命中规则提取
            tb = payload["pdf_meta"]["title_block"]
            self.assertIn("project", tb)
            self.assertIn("drawing_no", tb)
            self.assertIn("scale", tb)
            self.assertEqual(tb["scale"]["value"].strip("： :"), "1:100")
            # 矢量 PDF 应带 has_vector_geometry 与原生文字坐标元数据
            self.assertIn("has_vector_geometry", payload["pdf_meta"])
            self.assertEqual(payload["pdf_meta"]["has_vector_geometry"], payload["source_format"] == "pdf_vector")
            self.assertIn("vector_text_count", payload["pdf_meta"])
            self.assertIn("vector_text_items", payload["pdf_meta"])

            chk = subprocess.run(
                ["python3", str(VALIDATE), str(out_json)],
                capture_output=True, text=True, timeout=60,
            )
            self.assertIn('"ok": true', chk.stdout, chk.stdout + chk.stderr)

    def test_second_run_cache_hit(self):
        with tempfile.TemporaryDirectory(prefix="cad-pdfocr-test-") as tmp:
            workdir = Path(tmp)
            pdf = self._make_text_pdf(workdir)
            out = workdir / "out"
            subprocess.run([sys_py(), str(SCRIPT), str(pdf), "--out-dir", str(out)], capture_output=True, text=True, timeout=300, check=True)
            # 第二次运行不 force：文件级元数据命中；若 pdf 有 ocr_pages 页面缓存也应命中
            proc = subprocess.run(
                [sys_py(), str(SCRIPT), str(pdf), "--out-dir", str(out)],
                capture_output=True, text=True, timeout=300,
            )
            report = json.loads(proc.stdout)
            cache = report["results"][0].get("cache") or {}
            self.assertTrue(cache.get("file_meta_cached", False))

    def test_review_image_name_and_contract_with_review_image(self):
        # 第 3 步：_review 截图文件命名 + 带 review_image 字段的候选不破坏 v0 校验
        name = _review_image_name(_P("/tmp/一层平面图 2019.pdf"), 3)
        self.assertTrue(name.endswith("-p3.png"))
        self.assertIn("一层平面图", name)
        candidates = [{
            "id": "x1", "kind": "text", "value": None, "unit": None, "layer": None,
            "block_name": None, "text": "低置信行", "bbox": [0, 0, 5, 5],
            "evidence": [{"source": "local-ocr", "file": "a.pdf", "page": 3}],
            "method": "local-ocr-pixel", "confidence": 0.35, "confidence_tier": "review_required",
            "review_reasons": ["low_confidence_inference"], "review_notes": "低置信",
            "source_schema": "cad-file-reader/v0", "source_id": "a", "final_quantity": False,
            "rotation": None, "page_index": 3, "page_bbox": [0, 0, 5, 5],
            "source_format": "pdf_raster", "discipline_refs": [], "discipline_view_tags": [],
            "confidence_scores": {"ocr_confidence": 0.35}, "review_image": "_review/stem-p3.png",
        }]
        payload = build_contract(candidates, {"pdf_type": "scanned"}, "a.pdf", _P("/tmp/out"), False, "pdf_raster", {}, {"file_meta_cached": True})
        self.assertEqual(validate_contract_payload(payload), [])

    def test_scanned_candidates_writes_review_screenshots_for_low_confidence(self):
        # 第 3 步：低置信页触发 _review 截图，并带 review_image 字段
        import tempfile
        from unittest import mock
        from cad_pdf_ocr import scanned_candidates
        with tempfile.TemporaryDirectory(prefix="cad-pdf-review-test-") as tmp:
            root = _P(tmp)
            pdf = root / "scan.pdf"
            pdf.write_bytes(b"%%PDF-1.4 fake")
            cache_dir = root / "cache"
            review_dir = root / "out" / "_review"
            review_dir.mkdir(parents=True, exist_ok=True)
            entry = {"ocr_pages": [1]}
            with mock.patch("cad_pdf_ocr.ocr_page_cached",
                            return_value=([{"text": "低置信行", "conf": 0.30,
                                            "x0": 0.0, "y0": 0.0, "x1": 10.0, "y1": 5.0}], {})), \
                 mock.patch("cad_pdf_ocr.page_review_image",
                            side_effect=lambda _p, page, rd: (rd / f"scan-p{page}.png").touch() or (rd / f"scan-p{page}.png")):
                cands, _title, stats = scanned_candidates(
                    pdf, entry, str(pdf), cache_dir, "pdf_raster", 1, False, "0"*64, None, review_dir
                )
            self.assertEqual(len(cands), 1)
            self.assertEqual(cands[0]["review_image"], "_review/scan-p1.png")
            self.assertIn("low_confidence_inference", cands[0]["review_reasons"])
            self.assertIn(1, stats.get("review_pages", {}))
            self.assertTrue((review_dir / "scan-p1.png").exists())

import sys
sys.path.insert(0, str(ROOT / "scripts"))
from cad_pdf_ocr import extract_title_block_layout  # noqa: E402







class CadPdfTitleLayoutTest(unittest.TestCase):
    def test_layout_priority_uses_bottom_right_region(self):
        texts = [
            # 右下角图签栏（bbox y 小 = 图面下方）
            {"text": "图号：JD-01", "page_index": 1, "bbox": [10, 8, 200, 20], "confidence": 0.9},
            {"text": "项目名称：测试工程", "page_index": 1, "bbox": [10, 30, 260, 42], "confidence": 0.9},
            {"text": "比例：1:100", "page_index": 1, "bbox": [10, 52, 200, 64], "confidence": 0.95},
            # 图面上方干扰关键词，不应顶掉下方真实图签栏
            {"text": "图号：FAKE-TOP", "page_index": 1, "bbox": [400, 700, 520, 712], "confidence": 0.9},
        ]
        r = extract_title_block_layout(texts)
        self.assertEqual(r["drawing_no"]["value"], "JD-01")
        self.assertEqual(r["project"]["value"], "测试工程")
        self.assertEqual(r["scale"]["value"], "1:100")

    def test_no_bbox_falls_back_all_rows(self):
        texts = [
            {"text": "图名", "page_index": 1, "bbox": None, "confidence": 0.8},
            {"text": "图号：JD-99", "page_index": 1, "bbox": None, "confidence": 0.85},
            {"text": "比例：1:50", "page_index": 1, "bbox": None, "confidence": 0.85},
        ]
        r = extract_title_block_layout(texts)
        self.assertEqual(r["drawing_no"]["value"], "JD-99")
        self.assertEqual(r["scale"]["value"], "1:50")


    def test_two_line_label_value_pairing(self):
        texts = [
            {"text": "图名", "page_index": 1, "bbox": [10, 60, 60, 70], "confidence": 0.85},
            {"text": "一层平面图", "page_index": 1, "bbox": [10, 72, 90, 82], "confidence": 0.9},
            {"text": "比例", "page_index": 1, "bbox": [10, 40, 60, 50], "confidence": 0.85},
            {"text": "1:100", "page_index": 1, "bbox": [10, 52, 70, 62], "confidence": 0.9},
        ]
        r = extract_title_block_layout(texts)
        self.assertEqual(r["drawing_name"]["value"], "一层平面图")
        self.assertEqual(r["scale"]["value"], "1:100")




class CadPdfPageSelectionTest(unittest.TestCase):


    def setUp(self):
        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        from cad_pdf_ocr import _resolve_selected_pages, text_based_candidates
        self.resolve = _resolve_selected_pages
        self.text_cands = text_based_candidates

    def test_resolve_selected_pages(self):
        sel, invalid = self.resolve("1,3-5", 8)
        self.assertEqual(sel, {1, 3, 4, 5})
        self.assertEqual(invalid, [])
        sel, invalid = self.resolve("9,0", 8)
        self.assertIsNone(sel)
        self.assertEqual(invalid, [0, 9])
        sel, invalid = self.resolve("2-4", 3)
        self.assertEqual(sel, {2, 3})
        self.assertEqual(invalid, [])
        self.assertEqual(self.resolve(None, 3)[0], None)

    def test_text_based_page_detection_via_code_fences(self):
        with tempfile.TemporaryDirectory(prefix="cad-pdfpage-test-") as tmp:
            work = Path(tmp)
            md = work / "multi.md"
            md.write_text(
                "## Native text\n\n```\n图号:JD-01\n```\n\n```\n图号:JD-02\n```\n\n```\n图号:JD-03\n```\n",
                encoding="utf-8",
            )
            entry = {"markdown_file": str(md), "page_count": 3}
            cands, _ = self.text_cands(entry, work, "multi.pdf", "pdf_vector", None)
            self.assertEqual([c["page_index"] for c in cands], [1, 2, 3])
            self.assertEqual([c["text"] for c in cands], ["图号:JD-01", "图号:JD-02", "图号:JD-03"])

    def test_text_based_selected_pages_filter(self):
        with tempfile.TemporaryDirectory(prefix="cad-pdfpage-test-") as tmp:
            work = Path(tmp)
            md = work / "multi.md"
            md.write_text("```\n图号:JD-01\n```\n\n```\n图号:JD-02\n```\n", encoding="utf-8")
            entry = {"markdown_file": str(md), "page_count": 2}
            cands, _ = self.text_cands(entry, work, "multi.pdf", "pdf_vector", None, {2})
            self.assertEqual([c["text"] for c in cands], ["图号:JD-02"])
            self.assertEqual([c["page_index"] for c in cands], [2])



class CadPdfDisciplineTagTest(unittest.TestCase):
    def setUp(self):
        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        from cad_pdf_ocr import _infer_discipline_tags
        self.infer = _infer_discipline_tags

    def test_electrical_fire_hvac(self):
        self.assertIn("electrical", self.infer("配电箱 WL1 回路"))
        self.assertIn("fire_protection", self.infer("消火栓 2531"))
        self.assertIn("hvac_plumbing", self.infer("给排水 入户管"))

    def test_struct_and_site(self):
        self.assertIn("structural", self.infer("梁 KL1 C30 混凝土"))
        self.assertIn("site", self.infer("总图 场地坐标"))

    def test_no_hit(self):
        self.assertEqual(self.infer("图纸说明：详见设计说明"), [])


def sys_py() -> str:
    import sys as _sys
    return _sys.executable


if __name__ == "__main__":
    unittest.main()


class CadPdfBboxTest(unittest.TestCase):
    def test_px_to_pdf_bbox_scale(self):
        from cad_pdf_ocr import _px_to_pdf_bbox
        px = [0, 0, 200, 100]  # 200dpi 渲染，1in=200px => 1px=0.36pt
        pt = _px_to_pdf_bbox(px, dpi=200)
        self.assertIsNotNone(pt)
        self.assertEqual(pt, [0.0, 0.0, 72.0, 36.0])

    def test_px_to_pdf_bbox_none(self):
        from cad_pdf_ocr import _px_to_pdf_bbox
        self.assertIsNone(_px_to_pdf_bbox(None))
        self.assertIsNone(_px_to_pdf_bbox([1, 2, 3]))
