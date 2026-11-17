import hashlib
import sys
import unittest
sys.path.insert(0, "skills/agy-ppt/scripts")
sys.path.insert(0, "skills/agy-ppt/tests")
from ocr_providers import *
from ocr_providers.models import validate_locator
from helpers.fake_ocr_provider import FakeOCRProvider

SRC = hashlib.sha256(b"raw source").hexdigest()
CAP = OCRProviderCapabilities(True, True, "local", False)

def evidence(**kw):
    values = dict(schema_version="1.0", source_id="src", source_digest=SRC,
                  pages=(OCRPage({"kind":"page", "page":1}, "raw", ()),),
                  capabilities=CAP, provider=OCRProviderMetadata("fake", "1.0"),
                  provenance=OCRProvenance("fake", "fake", "local", False))
    values.update(kw)
    return OCREvidence(**values)

class OCRContractTests(unittest.TestCase):
    def test_geometry_free_and_empty_regions(self): evidence().validate()
    def test_raw_text_preserved_and_serialization_stable(self): self.assertEqual(evidence().to_json(), evidence().to_json())
    def test_canonical_hierarchy_and_no_flat_text_fields(self):
        payload = evidence().to_dict()
        self.assertIn("provider", payload); self.assertIn("pages", payload)
        self.assertEqual(payload["pages"][0]["raw_text"], "raw")
        self.assertNotIn("provider_id", payload); self.assertNotIn("raw_text", payload)
    def test_missing_capability_rejected(self):
        with self.assertRaises(OCRError) as c: OCRProviderCapabilities(False, True, "local", False).validate()
        self.assertEqual(c.exception.error_code, "OCR_PROVIDER_CAPABILITY_MISSING")
    def test_remote_privacy_rejected(self):
        with self.assertRaises(OCRError): OCRProviderCapabilities(True, True, "remote", False).validate()
    def test_invalid_locator_indices(self):
        for loc in ({"kind":"page","page":0},{"kind":"page","page":True},{"kind":"bad","page":1}):
            with self.assertRaises(OCRError): validate_locator(loc)
    def test_invalid_geometry_rejected(self):
        with self.assertRaises(OCRError): evidence(pages=(OCRPage({"kind":"page","page":1}, "raw", ({"region_id":"r","text":"x","bounding_box":{"x":0,"y":0,"width":2,"height":1}},)),)).validate()
    def test_provider_mismatch_rejected(self):
        with self.assertRaises(OCRError): evidence(provenance=OCRProvenance("fake", "other", "local", False)).validate()
    def test_unknown_version_rejected(self):
        with self.assertRaises(OCRError) as c: evidence(provider=OCRProviderMetadata("fake", "unknown")).validate()
        self.assertEqual(c.exception.error_code, "OCR_PROVIDER_VERSION_UNAVAILABLE")
    def test_model_manifest_order_and_digest(self):
        digest = "a" * 64
        evidence(model_manifest=({"model_id":"a","model_digest":digest},)).validate()
        with self.assertRaises(OCRError): evidence(model_manifest=({"model_id":"b"},{"model_id":"a"})).validate()
    def test_fake_provider_records_deterministic_call(self):
        p=FakeOCRProvider(); req=OCRRequest(b"img","src",SRC,{"kind":"image","ordinal":1})
        self.assertEqual(p.recognize(req).raw_text, "deterministic OCR text"); self.assertEqual(p.calls, [req])

if __name__ == "__main__": unittest.main()
