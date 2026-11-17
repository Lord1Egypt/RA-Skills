"""Deterministic provider selection and explicit, single-attempt fallback."""
from collections.abc import Mapping
from dataclasses import replace
from .base import OCRProvider
from .errors import OCRError
from .models import OCRRequest, OCRResolution, OCREvidence
from .validation import validate_evidence, validate_provider, validate_request

_TERMINAL = frozenset({
    "OCR_PROVIDER_NOT_FOUND", "OCR_PROVIDER_CONTRACT_INVALID",
    "OCR_PROVIDER_CAPABILITY_MISSING", "OCR_PROVIDER_VERSION_UNAVAILABLE",
    "OCR_PROVIDER_VERSION_UNSUPPORTED", "OCR_SOURCE_CHANGED", "OCR_MODEL_CHANGED",
    "OCR_LANGUAGE_UNSUPPORTED", "OCR_MODEL_UNAVAILABLE",
})
_ELIGIBLE = frozenset({
    "OCR_PROVIDER_UNAVAILABLE", "OCR_PROVIDER_FAILED", "OCR_PROVIDER_OUTPUT_INVALID",
    "OCR_EXTRACTION_FAILED",
})

def resolve_provider(providers: Mapping[str, OCRProvider], *, explicit: str | None = None,
                     project: str | None = None, user: str | None = None,
                     default: str = "tesseract") -> tuple[OCRProvider, OCRResolution]:
    for origin, provider_id in (("explicit", explicit), ("project", project), ("user", user), ("default", default)):
        if provider_id is not None:
            provider = providers.get(provider_id)
            if provider is None:
                raise OCRError(f"provider not found: {provider_id}", "OCR_PROVIDER_NOT_FOUND")
            validate_provider(provider)
            return provider, OCRResolution(provider_id, provider_id, selection_origin=origin)
    raise OCRError("no provider selected", "OCR_PROVIDER_NOT_FOUND")

def execute_with_fallback(providers: Mapping[str, OCRProvider], request: OCRRequest, *,
                          explicit: str | None = None, project: str | None = None,
                          user: str | None = None, default: str = "tesseract",
                          allow_fallback: bool = False) -> OCREvidence:
    validate_request(request)
    provider, resolution = resolve_provider(providers, explicit=explicit, project=project, user=user, default=default)
    try:
        evidence = provider.recognize(request)
        validate_evidence(evidence)
        if evidence.provenance.requested_provider != resolution.requested_provider:
            evidence = replace(evidence, provenance=replace(evidence.provenance, requested_provider=resolution.requested_provider, selection_origin=resolution.selection_origin))
        return evidence
    except OCRError as failure:
        if failure.error_code in _TERMINAL or resolution.actual_provider == default or not allow_fallback:
            if failure.error_code in _ELIGIBLE and not allow_fallback and resolution.actual_provider != default:
                raise OCRError("fallback is not allowed", "OCR_FALLBACK_NOT_ALLOWED", cause=failure) from failure
            raise
        if failure.error_code not in _ELIGIBLE:
            raise
        fallback = providers.get(default)
        if fallback is None:
            raise OCRError("fallback provider not found", "OCR_PROVIDER_NOT_FOUND", cause=failure) from failure
        validate_provider(fallback)
        try:
            result = fallback.recognize(request)
            validate_evidence(result)
            return replace(result, provenance=replace(result.provenance,
                requested_provider=resolution.requested_provider, actual_provider=fallback.provider_id,
                fallback_used=True, fallback_reason=failure.error_code,
                selection_origin=resolution.selection_origin))
        except OCRError as fallback_failure:
            raise fallback_failure from failure
