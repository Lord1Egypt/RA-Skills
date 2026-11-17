import hashlib, tempfile, unittest
from pathlib import Path
import sys
sys.path.insert(0, "skills/agy-ppt/scripts")
from ocr_providers import *

TSV="level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext\n1\t1\t0\t0\t0\t0\t0\t0\t20\t20\t-1\t\n5\t1\t1\t1\t1\t1\t0\t0\t10\t10\t90\tHello\n"
class Runner:
    def __init__(self): self.calls=[]
    def run(self, argv):
        self.calls.append(argv)
        if argv[-1:] == ["--version"]: return ProcessResult(0,"tesseract 5.3.0\n","")
        out=Path(argv[2]); out.with_suffix(".txt").write_text("Hello\n\n世界\n",encoding="utf-8"); out.with_suffix(".tsv").write_text(TSV,encoding="utf-8")
        return ProcessResult(0,"","")
class ExecutionTests(unittest.TestCase):
    def req(self): return OCRRequest(b"i","s",hashlib.sha256(b"raw").hexdigest(),{"kind":"image","ordinal":1},{"languages":"eng"})
    def test_raw_text_comes_from_engine_text_and_argv_is_safe(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d,"eng.traineddata").write_bytes(b"a"); r=Runner(); p=TesseractProvider("tesseract",runner=r,tessdata_dir=d)
            out=p.recognize(self.req()); self.assertEqual(out.raw_text,"Hello\n\n世界\n")
            call=r.calls[-1]; self.assertIn("-l",call); self.assertIn("eng",call); self.assertIn("--tessdata-dir",call)
    def test_model_change_prevents_recognition(self):
        with tempfile.TemporaryDirectory() as d:
            model=Path(d,"eng.traineddata"); model.write_bytes(b"a"); r=Runner(); p=TesseractProvider("tesseract",runner=r,tessdata_dir=d); expected=p.discover_traineddata("eng"); model.write_bytes(b"b")
            with self.assertRaises(OCRError) as c: p.recognize(self.req(),expected_models=expected)
            self.assertEqual(c.exception.error_code,"OCR_MODEL_CHANGED"); self.assertEqual(r.calls,[])
    def test_malformed_tsv_rejected(self):
        with self.assertRaises(OCRError) as c: parse_tsv("bad\theader\n")
        self.assertEqual(c.exception.error_code,"OCR_PROVIDER_OUTPUT_INVALID")
