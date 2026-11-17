import hashlib, sys, unittest
sys.path.insert(0, "skills/agy-ppt/scripts")
sys.path.insert(0, "skills/agy-ppt/tests")
from ocr_providers import *
from helpers.fake_ocr_provider import FakeOCRProvider

D = hashlib.sha256(b"raw").hexdigest()
REQ = OCRRequest(b"prepared", "s", D, {"kind":"image", "ordinal":1})

class ResolutionTests(unittest.TestCase):
    def providers(self):
        return {"explicit": FakeOCRProvider(text="explicit"), "project": FakeOCRProvider(text="project"),
                "user": FakeOCRProvider(text="user"), "tesseract": FakeOCRProvider(text="fallback")}
    def test_precedence_and_origin(self):
        p, r = resolve_provider(self.providers(), explicit="explicit", project="project", user="user")
        self.assertEqual((p.provider_id, r.selection_origin), ("fake", "explicit"))
        self.assertEqual(resolve_provider({"project": FakeOCRProvider()}, project="project", user="user")[1].selection_origin, "project")
        self.assertEqual(resolve_provider({"user": FakeOCRProvider()}, user="user")[1].selection_origin, "user")
        self.assertEqual(resolve_provider({"tesseract": FakeOCRProvider()})[1].selection_origin, "default")
    def test_selected_unknown_does_not_fall_through(self):
        with self.assertRaises(OCRError) as c: resolve_provider(self.providers(), explicit="missing", project="project")
        self.assertEqual(c.exception.error_code, "OCR_PROVIDER_NOT_FOUND")
    def test_unknown_project_user_and_default_are_stable_errors(self):
        for kwargs, providers in (({"project":"missing"}, self.providers()), ({"user":"missing"}, self.providers()), ({}, {})):
            with self.assertRaises(OCRError) as c: resolve_provider(providers, **kwargs)
            self.assertEqual(c.exception.error_code, "OCR_PROVIDER_NOT_FOUND")
    def test_operational_failure_disabled_preserves_cause(self):
        ps=self.providers(); ps["explicit"].fail_code="OCR_PROVIDER_FAILED"
        with self.assertRaises(OCRError) as c: execute_with_fallback(ps, REQ, explicit="explicit")
        self.assertEqual(c.exception.error_code, "OCR_FALLBACK_NOT_ALLOWED"); self.assertEqual(c.exception.cause.error_code, "OCR_PROVIDER_FAILED")
    def test_operational_failure_falls_back_once_with_provenance(self):
        ps=self.providers(); ps["explicit"].fail_code="OCR_PROVIDER_UNAVAILABLE"
        out=execute_with_fallback(ps, REQ, explicit="explicit", allow_fallback=True)
        self.assertEqual(out.raw_text, "fallback"); self.assertEqual(out.provenance.requested_provider, "explicit"); self.assertTrue(out.provenance.fallback_used)
        self.assertEqual(out.provenance.fallback_reason, "OCR_PROVIDER_UNAVAILABLE"); self.assertEqual(out.provenance.selection_origin, "explicit"); self.assertEqual(len(ps["tesseract"].calls), 1)
    def test_terminal_failure_never_falls_back(self):
        for code in ("OCR_PROVIDER_CONTRACT_INVALID", "OCR_PROVIDER_CAPABILITY_MISSING", "OCR_PROVIDER_VERSION_UNAVAILABLE", "OCR_PROVIDER_VERSION_UNSUPPORTED", "OCR_SOURCE_CHANGED", "OCR_MODEL_CHANGED"):
            ps=self.providers(); ps["explicit"].fail_code=code
            with self.assertRaises(OCRError) as c: execute_with_fallback(ps, REQ, explicit="explicit", allow_fallback=True)
            self.assertEqual(c.exception.error_code, code); self.assertEqual(ps["tesseract"].calls, [])
    def test_model_changed_never_becomes_fallback_not_allowed(self):
        ps=self.providers(); ps["explicit"].fail_code="OCR_MODEL_CHANGED"
        for allowed in (False, True):
            ps["tesseract"].calls.clear()
            with self.assertRaises(OCRError) as c: execute_with_fallback(ps, REQ, explicit="explicit", allow_fallback=allowed)
            self.assertEqual(c.exception.error_code, "OCR_MODEL_CHANGED"); self.assertEqual(ps["tesseract"].calls, [])
    def test_default_failure_does_not_recurse(self):
        ps=self.providers(); ps["tesseract"].fail_code="OCR_PROVIDER_FAILED"
        with self.assertRaises(OCRError) as c: execute_with_fallback(ps, REQ)
        self.assertEqual(c.exception.error_code, "OCR_PROVIDER_FAILED"); self.assertEqual(len(ps["tesseract"].calls), 1)
    def test_fallback_failure_terminates_without_retry(self):
        ps=self.providers(); ps["explicit"].fail_code="OCR_PROVIDER_FAILED"; ps["tesseract"].fail_code="OCR_PROVIDER_FAILED"
        with self.assertRaises(OCRError) as c: execute_with_fallback(ps, REQ, explicit="explicit", allow_fallback=True)
        self.assertEqual(c.exception.error_code, "OCR_PROVIDER_FAILED"); self.assertEqual(len(ps["tesseract"].calls), 1)

if __name__ == "__main__": unittest.main()
