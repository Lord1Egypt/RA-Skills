"""Public validation entry points for the Phase 15.1 contract."""
import re
from .base import OCRProvider
from .errors import OCRError
from .models import OCRRequest, OCREvidence, validate_locator

_DIGEST = re.compile(r"^[0-9a-f]{64}$")

def validate_provider(provider: OCRProvider) -> None:
    if not isinstance(getattr(provider, "provider_id", None), str) or not provider.provider_id:
        raise OCRError("provider_id is required", "OCR_PROVIDER_CONTRACT_INVALID")
    version = getattr(provider, "provider_version", None)
    if not isinstance(version, str) or not version or version.lower() == "unknown":
        raise OCRError("provider version is unavailable", "OCR_PROVIDER_VERSION_UNAVAILABLE")
    provider.capabilities.validate()

def validate_request(request: OCRRequest) -> None:
    if not isinstance(request.image_bytes, bytes) or not request.source_id or not _DIGEST.fullmatch(request.source_digest):
        raise OCRError("request requires bytes, source_id and raw-source SHA-256", "OCR_PROVIDER_CONTRACT_INVALID")
    validate_locator(request.locator)

def validate_evidence(evidence: OCREvidence) -> None:
    evidence.validate()
