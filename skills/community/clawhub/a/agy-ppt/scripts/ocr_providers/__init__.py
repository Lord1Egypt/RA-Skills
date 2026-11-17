"""Provider-neutral OCR contract primitives (Phase 15.1)."""

from .base import OCRProvider
from .errors import OCRError
from .models import (
    OCRDiagnostic, OCREvidence, OCRProviderCapabilities, OCRProvenance,
    OCRRequest, OCRResolution, OCRPage, OCRProviderMetadata,
)
from .validation import validate_evidence, validate_provider, validate_request
from .resolution import execute_with_fallback, resolve_provider
from .process import ProcessResult, ProcessRunner
from .tesseract import TesseractProvider, Traineddata, parse_tesseract_version, parse_tsv
from .management import (
    EffectiveOCRConfiguration, OCRConfigurationStore, OCRProviderConfiguration,
    OCRProviderManager, tesseract_validation_probe,
)

__all__ = [
    "OCRProvider", "OCRError", "OCRDiagnostic", "OCREvidence",
    "OCRProviderCapabilities", "OCRProvenance", "OCRRequest", "OCRResolution",
    "OCRPage", "OCRProviderMetadata",
    "validate_evidence", "validate_provider", "validate_request",
    "resolve_provider", "execute_with_fallback",
    "ProcessResult", "ProcessRunner", "TesseractProvider", "Traineddata", "parse_tesseract_version", "parse_tsv",
    "EffectiveOCRConfiguration", "OCRConfigurationStore", "OCRProviderConfiguration",
    "OCRProviderManager", "tesseract_validation_probe",
]
