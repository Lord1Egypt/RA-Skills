#!/usr/bin/env python3
"""Deterministic Phase 18 clean-plate worker and qualification contracts.

This module is deliberately runtime-independent from Jev.  Jev may classify
development fixtures, but live production and CI enforce the adopted rules
here without network access or credentials.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


ERROR_WORKER_CONTRACT_INVALID = "PHASE18_WORKER_CONTRACT_INVALID"


class WorkerContractError(ValueError):
    def __init__(self, error_code: str, message: str) -> None:
        super().__init__(message)
        self.error_code = error_code


class WorkerContractCompleteness(str, Enum):
    COMPLETE = "COMPLETE"
    PARTIAL = "PARTIAL"
    UNSAFE = "UNSAFE"


class QualificationEvidence(str, Enum):
    LIVE_VERIFIED = "LIVE_VERIFIED"
    PROXY_ONLY = "PROXY_ONLY"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


class ReservedZonePromptCompliance(str, Enum):
    CLEARLY_PROPAGATED = "CLEARLY_PROPAGATED"
    AMBIGUOUS = "AMBIGUOUS"
    MISSING = "MISSING"


class SampleProvenance(str, Enum):
    RAW_PLATE = "RAW_PLATE"
    HYBRID_PREVIEW = "HYBRID_PREVIEW"
    AMBIGUOUS = "AMBIGUOUS"


_MODES = frozenset({"CLEAN_PLATE", "PARTIAL_COMPOSITE", "FULL_COMPOSITE"})
_NATIVE_STRATEGIES = frozenset({"NATIVE_TEXT", "NATIVE_IMAGE", "NATIVE_CHART", "NATIVE_SHAPE", "VECTOR_GRAPHIC"})
_CONTENT_TYPES = frozenset({"text", "image", "chart", "shape", "visual"})
_REQUIRED_MANIFEST_KEYS = frozenset({
    "slide_id", "plate_mode", "reserved_zones", "locked_content_to_render",
    "editable_content_to_omit", "replaceable_assets_to_omit", "background_instructions",
})


def canonical_json(value: Mapping[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def manifest_sha256(manifest: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_json(manifest).encode("utf-8")).hexdigest()


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_box(value: Any) -> bool:
    if not isinstance(value, Mapping):
        return False
    try:
        numbers = tuple(float(value[key]) for key in ("left", "top", "width", "height"))
    except (KeyError, TypeError, ValueError):
        return False
    return numbers[0] >= 0 and numbers[1] >= 0 and numbers[2] > 0 and numbers[3] > 0


@dataclass(frozen=True)
class WorkerContractAudit:
    status: WorkerContractCompleteness
    findings: tuple[str, ...]
    manifest_hash: str | None = None


def audit_worker_contract(manifest: Mapping[str, Any] | None) -> WorkerContractAudit:
    """Classify a serialized :class:`VisualPlateJobSpec` without fuzzy repair."""
    if not isinstance(manifest, Mapping):
        return WorkerContractAudit(WorkerContractCompleteness.UNSAFE, ("manifest_missing",))
    missing = sorted(_REQUIRED_MANIFEST_KEYS - set(manifest))
    if missing:
        return WorkerContractAudit(
            WorkerContractCompleteness.UNSAFE,
            tuple(f"missing:{key}" for key in missing),
        )
    if not _nonempty_string(manifest.get("slide_id")):
        return WorkerContractAudit(WorkerContractCompleteness.UNSAFE, ("slide_id_invalid",))
    mode = manifest.get("plate_mode")
    if mode not in _MODES:
        return WorkerContractAudit(WorkerContractCompleteness.UNSAFE, ("plate_mode_invalid",))
    zones = manifest.get("reserved_zones")
    omit_editable = manifest.get("editable_content_to_omit")
    omit_assets = manifest.get("replaceable_assets_to_omit")
    locked = manifest.get("locked_content_to_render")
    if not all(isinstance(value, list) for value in (zones, omit_editable, omit_assets, locked)):
        return WorkerContractAudit(WorkerContractCompleteness.UNSAFE, ("manifest_lists_invalid",))
    if mode == "FULL_COMPOSITE" and (zones or omit_editable or omit_assets):
        return WorkerContractAudit(
            WorkerContractCompleteness.UNSAFE,
            ("full_composite_cannot_receive_native_overlays",),
        )

    findings: list[str] = []
    zone_ids: set[str] = set()
    for index, zone in enumerate(zones):
        prefix = f"zone[{index}]"
        if not isinstance(zone, Mapping):
            return WorkerContractAudit(WorkerContractCompleteness.UNSAFE, (f"{prefix}:invalid",))
        for field in ("zone_id", "slide_id", "element_id", "role", "strategy", "expected_content_type", "plate_requirement"):
            if not _nonempty_string(zone.get(field)):
                return WorkerContractAudit(WorkerContractCompleteness.UNSAFE, (f"{prefix}:{field}_invalid",))
        if zone["slide_id"] != manifest["slide_id"]:
            return WorkerContractAudit(WorkerContractCompleteness.UNSAFE, (f"{prefix}:slide_mismatch",))
        if zone["zone_id"] in zone_ids:
            return WorkerContractAudit(WorkerContractCompleteness.UNSAFE, (f"{prefix}:duplicate_id",))
        zone_ids.add(str(zone["zone_id"]))
        if zone["strategy"] not in _NATIVE_STRATEGIES:
            return WorkerContractAudit(WorkerContractCompleteness.UNSAFE, (f"{prefix}:strategy_not_native",))
        if zone["expected_content_type"] not in _CONTENT_TYPES:
            return WorkerContractAudit(WorkerContractCompleteness.UNSAFE, (f"{prefix}:content_type_invalid",))
        if zone["plate_requirement"] != "CONTENT_FREE":
            return WorkerContractAudit(WorkerContractCompleteness.UNSAFE, (f"{prefix}:content_free_required",))
        if not _valid_box(zone.get("box")):
            return WorkerContractAudit(WorkerContractCompleteness.UNSAFE, (f"{prefix}:box_invalid",))
        if not _nonempty_string(zone.get("background_treatment")):
            findings.append(f"{prefix}:background_treatment_missing")

    omitted_count = len(omit_editable) + len(omit_assets)
    if mode in {"CLEAN_PLATE", "PARTIAL_COMPOSITE"} and omitted_count and not zones:
        return WorkerContractAudit(WorkerContractCompleteness.UNSAFE, ("omitted_content_has_no_reserved_zone",))
    if zones and omitted_count < len(zones):
        findings.append("reserved_zone_omission_count_mismatch")
    status = WorkerContractCompleteness.PARTIAL if findings else WorkerContractCompleteness.COMPLETE
    return WorkerContractAudit(status, tuple(findings), manifest_sha256(manifest))


def render_reserved_zone_contract(manifest: Mapping[str, Any]) -> str:
    audit = audit_worker_contract(manifest)
    if audit.status is not WorkerContractCompleteness.COMPLETE:
        raise WorkerContractError(
            ERROR_WORKER_CONTRACT_INVALID,
            "visual plate job must be COMPLETE before worker dispatch: " + ", ".join(audit.findings),
        )
    lines = [
        "## Reserved Editable Zone Contract (mandatory)",
        f"Manifest SHA-256: {audit.manifest_hash}",
        f"Plate mode: {manifest['plate_mode']}",
        "The output is a visual plate, not a completed slide.",
        "Every CONTENT_FREE zone below must remain free of its semantic content.",
        "Do not draw, print, ghost, watermark, or bake the corresponding text, number, logo, photo, chart, or CTA into that zone.",
        "Continue the approved background treatment through each zone unless its instruction says transparent.",
    ]
    for zone in manifest["reserved_zones"]:
        box = zone["box"]
        lines.append(
            "- "
            f"{zone['zone_id']} | element={zone['element_id']} | role={zone['role']} | "
            f"type={zone['expected_content_type']} | strategy={zone['strategy']} | "
            f"requirement=CONTENT_FREE | box_inches=({box['left']},{box['top']},{box['width']},{box['height']}) | "
            f"background={zone['background_treatment']}"
        )
    if manifest["editable_content_to_omit"]:
        lines.append("Editable content to omit from the plate: " + json.dumps(manifest["editable_content_to_omit"], ensure_ascii=False))
    if manifest["replaceable_assets_to_omit"]:
        lines.append("Replaceable assets to omit from the plate: " + json.dumps(manifest["replaceable_assets_to_omit"], ensure_ascii=False))
    if manifest["locked_content_to_render"]:
        lines.append("Locked content that must remain rendered in the plate: " + json.dumps(manifest["locked_content_to_render"], ensure_ascii=False))
    if str(manifest.get("background_instructions") or "").strip():
        lines.append("Background instructions: " + str(manifest["background_instructions"]).strip())
    lines.append("If any reserved zone cannot be kept content-free, return COMPOSITE_CONFLICT and do not generate an image.")
    return "\n".join(lines)


def classify_reserved_zone_prompt(prompt: str, manifest: Mapping[str, Any] | None) -> ReservedZonePromptCompliance:
    audit = audit_worker_contract(manifest)
    if audit.status is WorkerContractCompleteness.UNSAFE or not isinstance(prompt, str):
        return ReservedZonePromptCompliance.MISSING
    required = ("Reserved Editable Zone Contract", "CONTENT_FREE", str(audit.manifest_hash), "COMPOSITE_CONFLICT")
    if not all(token in prompt for token in required):
        return ReservedZonePromptCompliance.MISSING
    zone_tokens = [str(zone["zone_id"]) for zone in manifest["reserved_zones"]]
    if all(token in prompt for token in zone_tokens) and audit.status is WorkerContractCompleteness.COMPLETE:
        return ReservedZonePromptCompliance.CLEARLY_PROPAGATED
    return ReservedZonePromptCompliance.AMBIGUOUS


def classify_qualification_evidence(record: Mapping[str, Any] | None) -> QualificationEvidence:
    if not isinstance(record, Mapping):
        return QualificationEvidence.INSUFFICIENT_EVIDENCE
    diagnostics = record.get("diagnostics")
    if not isinstance(diagnostics, Mapping):
        diagnostics = {}
    def field(name: str) -> Any:
        return record.get(name) if record.get(name) is not None else diagnostics.get(name)
    if field("proxy") is True or field("worker_kind") in {"callback", "fake", "proxy", "agy_native"}:
        return QualificationEvidence.PROXY_ONLY
    required = (
        "dispatch_id", "job_id", "thread_id", "worker_result_id", "plate_artifact_sha256",
        "reserved_zone_manifest_sha256", "output_artifact_sha256",
    )
    if field("backend") == "codex_builtin_imagegen" and field("status") == "completed" and all(
        _nonempty_string(field(key)) for key in required
    ):
        return QualificationEvidence.LIVE_VERIFIED
    return QualificationEvidence.INSUFFICIENT_EVIDENCE


def classify_sample_provenance(record: Mapping[str, Any] | None) -> SampleProvenance:
    if not isinstance(record, Mapping):
        return SampleProvenance.AMBIGUOUS
    kind = record.get("artifact_kind")
    if kind == "RAW_PLATE" and _nonempty_string(record.get("plate_artifact_sha256")):
        return SampleProvenance.RAW_PLATE
    if kind == "HYBRID_PREVIEW" and all(
        _nonempty_string(record.get(key))
        for key in ("artifact_ref", "hybrid_manifest_sha256", "rendered_preview_sha256")
    ):
        return SampleProvenance.HYBRID_PREVIEW
    return SampleProvenance.AMBIGUOUS


__all__ = [
    "ERROR_WORKER_CONTRACT_INVALID", "QualificationEvidence", "ReservedZonePromptCompliance",
    "SampleProvenance", "WorkerContractAudit", "WorkerContractCompleteness", "WorkerContractError",
    "audit_worker_contract", "classify_qualification_evidence", "classify_reserved_zone_prompt",
    "classify_sample_provenance", "manifest_sha256", "render_reserved_zone_contract",
]
