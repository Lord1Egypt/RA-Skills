"""Immutable, serializable provider-neutral OCR contract models."""
from dataclasses import dataclass, field
from typing import Any, Mapping
import json
import math
import re
from types import MappingProxyType

from .errors import OCRError

_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_REQUIRED_CAPS = ("text", "locators")
SELECTION_ORIGINS = frozenset({"explicit", "project", "user", "default"})

def _invalid(message: str) -> OCRError:
    return OCRError(message, "OCR_PROVIDER_CONTRACT_INVALID")

def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({k: _freeze(v) for k, v in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(v) for v in value)
    return value

def _plain(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {k: _plain(v) for k, v in value.items()}
    if isinstance(value, tuple):
        return [_plain(v) for v in value]
    return value

@dataclass(frozen=True)
class OCRProviderCapabilities:
    text: bool
    locators: bool
    execution_location: str
    source_may_leave_local_machine: bool
    bounding_boxes: bool = False
    confidence: bool = False
    word_boxes: bool = False
    orientation: bool = False
    tables: bool = False
    layout_regions: bool = False

    def validate(self) -> None:
        if not isinstance(self.text, bool) or not isinstance(self.locators, bool) or not self.text or not self.locators:
            raise OCRError("text and locators capabilities are required", "OCR_PROVIDER_CAPABILITY_MISSING")
        if self.execution_location not in ("local", "remote"):
            raise _invalid("execution_location must be local or remote")
        if not isinstance(self.source_may_leave_local_machine, bool):
            raise _invalid("source_may_leave_local_machine must be boolean")
        if self.execution_location == "remote" and not self.source_may_leave_local_machine:
            raise _invalid("remote providers must declare source may leave local machine")

@dataclass(frozen=True)
class OCRRequest:
    image_bytes: bytes
    source_id: str
    source_digest: str
    locator: Mapping[str, Any]
    language_config: Mapping[str, Any] = field(default_factory=dict)
    execution_config: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "locator", _freeze(self.locator))
        object.__setattr__(self, "language_config", _freeze(self.language_config))
        object.__setattr__(self, "execution_config", _freeze(self.execution_config))

@dataclass(frozen=True)
class OCRProvenance:
    requested_provider: str
    actual_provider: str
    execution_location: str
    source_may_leave_local_machine: bool
    fallback_used: bool = False
    fallback_reason: str | None = None
    selection_origin: str | None = None

@dataclass(frozen=True)
class OCRDiagnostic:
    error_code: str
    message: str
    cause: str | None = None

@dataclass(frozen=True)
class OCRResolution:
    requested_provider: str
    actual_provider: str
    fallback_used: bool = False
    fallback_reason: str | None = None
    selection_origin: str | None = None

@dataclass(frozen=True)
class OCRPage:
    locator: Mapping[str, Any]
    raw_text: str
    regions: tuple[Mapping[str, Any], ...]
    high_risk_signals: tuple[Mapping[str, Any], ...] = ()

    def __post_init__(self) -> None:
        for name in ("locator", "regions", "high_risk_signals"):
            object.__setattr__(self, name, _freeze(getattr(self, name)))

@dataclass(frozen=True)
class OCRProviderMetadata:
    provider_id: str
    provider_version: str
    engine_name: str | None = None
    engine_version: str | None = None

@dataclass(frozen=True)
class OCREvidence:
    schema_version: str
    source_id: str
    source_digest: str
    pages: tuple[OCRPage, ...]
    capabilities: OCRProviderCapabilities
    provider: OCRProviderMetadata
    provenance: OCRProvenance
    model_manifest: tuple[Mapping[str, Any], ...] = ()
    language_config: Mapping[str, Any] = field(default_factory=dict)
    execution_config: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("language_config", "execution_config"):
            object.__setattr__(self, name, _freeze(getattr(self, name)))

    @property
    def raw_text(self) -> str:
        return self.pages[0].raw_text if len(self.pages) == 1 else ""
        for name in ("pages", "model_manifest"):
            object.__setattr__(self, name, _freeze(getattr(self, name)))

    def validate(self) -> None:
        if not self.schema_version or not self.source_id or not _DIGEST.fullmatch(self.source_digest):
            raise _invalid("schema_version, source_id and lowercase SHA-256 source_digest are required")
        self.capabilities.validate()
        if not self.provider.provider_id:
            raise _invalid("provider_id is required")
        if not self.provider.provider_version or self.provider.provider_version.lower() == "unknown":
            raise OCRError("provider version is required", "OCR_PROVIDER_VERSION_UNAVAILABLE")
        if self.provider.engine_name and (not self.provider.engine_version or self.provider.engine_version.lower() == "unknown"):
            raise OCRError("engine version is required", "OCR_PROVIDER_VERSION_UNAVAILABLE")
        if self.provenance.actual_provider != self.provider.provider_id:
            raise _invalid("provenance actual provider must match provider_id")
        if self.provenance.selection_origin is not None and self.provenance.selection_origin not in SELECTION_ORIGINS:
            raise _invalid("invalid provider selection origin")
        if self.provenance.execution_location != self.capabilities.execution_location:
            raise _invalid("provenance execution location mismatch")
        if self.provenance.source_may_leave_local_machine != self.capabilities.source_may_leave_local_machine:
            raise _invalid("provenance privacy declaration mismatch")
        if self.provenance.fallback_used != (self.provenance.fallback_reason is not None):
            raise _invalid("fallback provenance is inconsistent")
        _validate_models(self.model_manifest)
        for page in self.pages:
            validate_locator(page.locator)
            if not isinstance(page.raw_text, str):
                raise _invalid("raw_text must be a string")
            for region in page.regions:
                if not isinstance(region, Mapping) or not region.get("region_id") or not isinstance(region.get("text"), str):
                    raise _invalid("regions require region_id and text")
                if "bounding_box" in region:
                    _validate_box(region["bounding_box"])
                if "confidence" in region:
                    _validate_confidence(region["confidence"])

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return {"schema_version": self.schema_version, "source_id": self.source_id,
                "source_digest": self.source_digest,
                "pages": [{"locator": _plain(p.locator), "raw_text": p.raw_text,
                           "regions": _plain(p.regions),
                           **({"high_risk_signals": _plain(p.high_risk_signals)} if p.high_risk_signals else {})} for p in self.pages],
                "capabilities": dict(vars(self.capabilities)),
                "provider": {k: v for k, v in vars(self.provider).items() if v is not None},
                "provenance": {k: v for k, v in vars(self.provenance).items() if v is not None or k == "fallback_reason"},
                "model_manifest": _plain(self.model_manifest),
                "language_config": _plain(self.language_config), "execution_config": _plain(self.execution_config)}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)

def validate_locator(locator: Mapping[str, Any]) -> None:
    if not isinstance(locator, Mapping) or locator.get("kind") not in ("page", "image"):
        raise _invalid("invalid OCR-native locator kind")
    key = "page" if locator["kind"] == "page" else "ordinal"
    value = locator.get(key)
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise _invalid("locator index must be a positive integer")
    if "total_pages" in locator and (isinstance(locator["total_pages"], bool) or not isinstance(locator["total_pages"], int) or locator["total_pages"] < value):
        raise _invalid("total_pages must not be less than page")

def _validate_box(box: Any) -> None:
    if not isinstance(box, Mapping) or set(box) != {"x", "y", "width", "height"}:
        raise _invalid("bounding_box must contain x,y,width,height")
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or not 0 <= v <= 1 for v in box.values()):
        raise _invalid("bounding_box values must be finite and normalized")
    if box["x"] + box["width"] > 1 or box["y"] + box["height"] > 1:
        raise _invalid("bounding_box exceeds normalized bounds")

def _validate_confidence(value: Any) -> None:
    if not isinstance(value, Mapping) or not isinstance(value.get("raw_confidence"), (int, float)) or not math.isfinite(value["raw_confidence"]):
        raise _invalid("confidence metadata is invalid")
    if not value.get("confidence_scale") or not value.get("confidence_source"):
        raise _invalid("confidence scale and source are required")

def _validate_models(models: tuple[Mapping[str, Any], ...]) -> None:
    ids = []
    for model in models:
        if not isinstance(model, Mapping) or not model.get("model_id"):
            raise _invalid("model manifest entries require model_id")
        if "model_digest" in model and (not isinstance(model["model_digest"], str) or not _DIGEST.fullmatch(model["model_digest"])):
            raise _invalid("model_digest must be lowercase SHA-256")
        ids.append(model["model_id"])
    if len(ids) != len(set(ids)) or list(models) != sorted(models, key=lambda m: (m.get("model_id", ""), m.get("model_version", ""), m.get("model_digest", ""), m.get("model_source", ""))):
        raise _invalid("model manifest must be unique and deterministically ordered")
