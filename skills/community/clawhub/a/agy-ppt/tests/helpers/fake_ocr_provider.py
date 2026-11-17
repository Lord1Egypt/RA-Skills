"""Deterministic fake OCR provider for contract tests."""
from dataclasses import dataclass, field
from typing import Any
import hashlib
import sys
sys.path.insert(0, "skills/agy-ppt/scripts")
from ocr_providers import OCRProvider, OCRProviderCapabilities, OCRRequest, OCREvidence, OCRProvenance, OCRPage, OCRProviderMetadata, OCRError

@dataclass
class FakeOCRProvider(OCRProvider):
    text: str = "deterministic OCR text"
    with_geometry: bool = False
    calls: list[OCRRequest] = field(default_factory=list)
    fail_code: str | None = None
    provider_id: str = "fake"
    provider_version: str = "1.0.0"

    @property
    def capabilities(self):
        return OCRProviderCapabilities(True, True, "local", False, bounding_boxes=self.with_geometry)

    def recognize(self, request):
        self.calls.append(request)
        if self.fail_code:
            raise OCRError("injected fake failure", self.fail_code)
        regions = () if not self.with_geometry else ({"region_id": "r1", "text": self.text, "bounding_box": {"x": 0.0, "y": 0.0, "width": 1.0, "height": 1.0}},)
        evidence = OCREvidence("1.0", request.source_id, request.source_digest, (OCRPage(request.locator, self.text, tuple(regions)),), self.capabilities, OCRProviderMetadata(self.provider_id, self.provider_version), OCRProvenance(self.provider_id, self.provider_id, "local", False), language_config=request.language_config, execution_config=request.execution_config)
        evidence.validate()
        return evidence
