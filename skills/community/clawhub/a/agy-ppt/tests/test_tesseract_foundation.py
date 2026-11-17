import hashlib, tempfile, unittest
from pathlib import Path
import sys
sys.path.insert(0, "skills/agy-ppt/scripts")
from ocr_providers import OCRError, ProcessResult, TesseractProvider, parse_tesseract_version

class FakeRunner:
    def __init__(self, result): self.result=result; self.calls=[]
    def run(self, argv): self.calls.append(argv); return self.result

class TesseractFoundationTests(unittest.TestCase):
    def test_version_parsing_supported_and_multidigit(self): self.assertEqual(parse_tesseract_version("tesseract 5.12.3\nleptonica-1.84"), "5.12.3")
    def test_version_errors(self):
        for text, code in (("", "OCR_PROVIDER_VERSION_UNAVAILABLE"),("garbage", "OCR_PROVIDER_VERSION_UNAVAILABLE"),("tesseract 4.1.1", "OCR_PROVIDER_VERSION_UNSUPPORTED")):
            with self.assertRaises(OCRError) as c: parse_tesseract_version(text)
            self.assertEqual(c.exception.error_code, code)
    def test_probe_uses_argv_and_nonzero_is_version_unavailable(self):
        runner=FakeRunner(ProcessResult(0, "tesseract 5.3.0\n", "")); p=TesseractProvider("/safe/tesseract", runner=runner)
        self.assertEqual(p.detect_version(), "5.3.0"); self.assertEqual(runner.calls, [["/safe/tesseract", "--version"]])
        with self.assertRaises(OCRError) as c: TesseractProvider("x", runner=FakeRunner(ProcessResult(1,"tesseract 5.3.0","err"))).detect_version()
        self.assertEqual(c.exception.error_code, "OCR_PROVIDER_VERSION_UNAVAILABLE")
    def test_traineddata_digest_and_order_without_paths(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d,"eng.traineddata").write_bytes(b"eng"); Path(d,"chi_tra.traineddata").write_bytes(b"chi")
            models=TesseractProvider(tessdata_dir=d).discover_traineddata("chi_tra+eng")
            self.assertEqual([m.model_id for m in models], ["chi_tra", "eng"])
            self.assertEqual(models[1].model_digest, hashlib.sha256(b"eng").hexdigest()); self.assertNotIn(d, models[0].model_source)
    def test_missing_traineddata_is_stable_error(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(OCRError) as c: TesseractProvider(tessdata_dir=d).discover_traineddata("eng")
            self.assertEqual(c.exception.error_code, "OCR_MODEL_UNAVAILABLE")

if __name__ == "__main__": unittest.main()
