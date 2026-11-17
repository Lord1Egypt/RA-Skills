#!/usr/bin/env python3
"""Exact-artifact visual qualification for v0.6 presentation hardening.

The module does not pretend to measure beauty.  It records which concrete
artifact was inspected at each production stage, localizes material loss, and
keeps automated assistance subordinate to exact-artifact human acceptance.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from human_presentation_quality import (
    HumanPresentationQualityRecord,
    automated_quality_assistance,
)
from presentation_workflow import SampleArtifact


ERROR_VISUAL_QUALIFICATION_INVALID = "PRESENTATION_VISUAL_QUALIFICATION_INVALID"


class VisualStage(str, Enum):
    RAW_PLATE = "RAW_PLATE"
    HYBRID_PREVIEW = "HYBRID_PREVIEW"
    ACTUAL_CLIENT_RENDER = "ACTUAL_CLIENT_RENDER"


class VisualIssue(str, Enum):
    FONT = "FONT"
    GLYPH = "GLYPH"
    REFLOW = "REFLOW"
    OVERFLOW = "OVERFLOW"
    CROP = "CROP"
    POSITION = "POSITION"
    Z_ORDER = "Z_ORDER"
    CHART = "CHART"
    COLOR = "COLOR"
    HIERARCHY = "HIERARCHY"
    IMAGE = "IMAGE"
    OTHER = "OTHER"


class VisualDisposition(str, Enum):
    ACCEPT = "ACCEPT"
    WARNING = "WARNING"
    REPAIR = "REPAIR"
    BLOCK = "BLOCK"


class MaterialDegradation(str, Enum):
    NO_MATERIAL_DEGRADATION = "NO_MATERIAL_DEGRADATION"
    MINOR_DRIFT = "MINOR_DRIFT"
    MATERIAL_DEGRADATION = "MATERIAL_DEGRADATION"
    UNACCEPTABLE = "UNACCEPTABLE"


class CompositionDensity(str, Enum):
    """Bounded development-time classification, never a release score."""

    INTENTIONAL_MINIMAL = "INTENTIONAL_MINIMAL"
    BALANCED = "BALANCED"
    UNDERFILLED = "UNDERFILLED"
    OVERCROWDED = "OVERCROWDED"


class VisualAnchor(str, Enum):
    """Strength of the composition's primary visual point of entry."""

    STRONG = "STRONG"
    ADEQUATE = "ADEQUATE"
    WEAK = "WEAK"
    ABSENT = "ABSENT"


class CardInformationDepth(str, Enum):
    """Meaning carried inside a card, independent of the number of cards."""

    LABEL_ONLY = "LABEL_ONLY"
    SUPPORTING = "SUPPORTING"
    SUBSTANTIVE = "SUBSTANTIVE"


class ImageVariety(str, Enum):
    """Informational relationship among images used in a composition."""

    DISTINCT_INFORMATIONAL = "DISTINCT_INFORMATIONAL"
    RELATED_DETAIL = "RELATED_DETAIL"
    DUPLICATIVE = "DUPLICATIVE"
    DECORATIVE = "DECORATIVE"


class SemanticDensity(str, Enum):
    """Bounded semantic-depth classification; never inferred from object count."""

    LOW = "LOW"
    BALANCED = "BALANCED"
    HIGH = "HIGH"


class TextDensitySignal(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"


class VisualRoleExpectation(str, Enum):
    COVER_HERO = "COVER_HERO"
    BALANCED_EVIDENCE = "BALANCED_EVIDENCE"
    IMAGE_WITH_TAKEAWAYS = "IMAGE_WITH_TAKEAWAYS"
    ACTION_FLOW = "ACTION_FLOW"
    OTHER = "OTHER"


class CompositionSignalFinding(str, Enum):
    """Deterministic prompts for review, not an aesthetic verdict."""

    LOW_FOREGROUND_OBJECT_COUNT = "LOW_FOREGROUND_OBJECT_COUNT"
    SHALLOW_HIERARCHY = "SHALLOW_HIERARCHY"
    NARROW_OCCUPIED_ENVELOPE = "NARROW_OCCUPIED_ENVELOPE"
    MISSING_HERO_VISUAL = "MISSING_HERO_VISUAL"
    MISSING_PRIMARY_ANCHOR = "MISSING_PRIMARY_ANCHOR"
    LOW_TEXT_DENSITY_FOR_ROLE = "LOW_TEXT_DENSITY_FOR_ROLE"
    ROLE_STRUCTURE_MISSING = "ROLE_STRUCTURE_MISSING"


class EffectiveDensitySignalFinding(str, Enum):
    """Deterministic review prompts for effective, rather than raw, density."""

    LABEL_ONLY_CARD_PRESENT = "LABEL_ONLY_CARD_PRESENT"
    CARD_SUPPORTING_LAYER_MISSING = "CARD_SUPPORTING_LAYER_MISSING"
    DUPLICATIVE_IMAGE_PRESENT = "DUPLICATIVE_IMAGE_PRESENT"
    DECORATIVE_IMAGE_PRESENT = "DECORATIVE_IMAGE_PRESENT"
    IMAGE_VARIETY_MISSING = "IMAGE_VARIETY_MISSING"
    ROLE_SUPPORTING_LAYER_MISSING = "ROLE_SUPPORTING_LAYER_MISSING"


@dataclass(frozen=True)
class OccupiedContentEnvelope:
    """Normalized bounds of intentional foreground content."""

    left: float
    top: float
    right: float
    bottom: float

    def __post_init__(self) -> None:
        values = (self.left, self.top, self.right, self.bottom)
        if any(
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            or not 0 <= float(value) <= 1
            for value in values
        ):
            raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
        if self.left >= self.right or self.top >= self.bottom:
            raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)

    @property
    def width(self) -> float:
        return float(self.right - self.left)

    @property
    def height(self) -> float:
        return float(self.bottom - self.top)


@dataclass(frozen=True)
class CompositionSignals:
    """Deterministic context supplied to Jev/Codex composition review."""

    foreground_object_count: int
    occupied_content_envelope: OccupiedContentEnvelope
    hierarchy_levels: int
    has_hero_visual: bool
    has_primary_numeric_or_graphic_anchor: bool
    text_density: TextDensitySignal
    visual_role_expectation: VisualRoleExpectation
    structured_visual_groups: int = 0

    def __post_init__(self) -> None:
        if (
            not isinstance(self.foreground_object_count, int)
            or isinstance(self.foreground_object_count, bool)
            or self.foreground_object_count < 0
            or not isinstance(self.hierarchy_levels, int)
            or isinstance(self.hierarchy_levels, bool)
            or self.hierarchy_levels < 0
            or not isinstance(self.structured_visual_groups, int)
            or isinstance(self.structured_visual_groups, bool)
            or self.structured_visual_groups < 0
            or not isinstance(self.occupied_content_envelope, OccupiedContentEnvelope)
            or not isinstance(self.has_hero_visual, bool)
            or not isinstance(self.has_primary_numeric_or_graphic_anchor, bool)
            or not isinstance(self.text_density, TextDensitySignal)
            or not isinstance(self.visual_role_expectation, VisualRoleExpectation)
        ):
            raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)


@dataclass(frozen=True)
class CompositionAssessment:
    """Reviewed bounded decision attached to exact rendered evidence."""

    slide_id: str
    artifact_sha256: str
    density: CompositionDensity
    visual_anchor: VisualAnchor
    signals: CompositionSignals
    rationale: str

    def __post_init__(self) -> None:
        if not re.fullmatch(r"slide_\d+", self.slide_id or ""):
            raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
        object.__setattr__(self, "artifact_sha256", _sha(self.artifact_sha256))
        if (
            not isinstance(self.density, CompositionDensity)
            or not isinstance(self.visual_anchor, VisualAnchor)
            or not isinstance(self.signals, CompositionSignals)
            or not isinstance(self.rationale, str)
            or not self.rationale.strip()
        ):
            raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)


def composition_signal_findings(signals: CompositionSignals) -> tuple[CompositionSignalFinding, ...]:
    """Return deterministic review prompts without deriving an aesthetic score."""
    if not isinstance(signals, CompositionSignals):
        raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
    findings: list[CompositionSignalFinding] = []
    if signals.foreground_object_count < 3:
        findings.append(CompositionSignalFinding.LOW_FOREGROUND_OBJECT_COUNT)
    if signals.hierarchy_levels < 2:
        findings.append(CompositionSignalFinding.SHALLOW_HIERARCHY)
    if signals.occupied_content_envelope.height < 0.35:
        findings.append(CompositionSignalFinding.NARROW_OCCUPIED_ENVELOPE)
    if signals.visual_role_expectation is VisualRoleExpectation.COVER_HERO and not signals.has_hero_visual:
        findings.append(CompositionSignalFinding.MISSING_HERO_VISUAL)
    if not (signals.has_hero_visual or signals.has_primary_numeric_or_graphic_anchor):
        findings.append(CompositionSignalFinding.MISSING_PRIMARY_ANCHOR)
    if (
        signals.text_density is TextDensitySignal.LOW
        and signals.visual_role_expectation in {
            VisualRoleExpectation.BALANCED_EVIDENCE,
            VisualRoleExpectation.IMAGE_WITH_TAKEAWAYS,
            VisualRoleExpectation.ACTION_FLOW,
        }
    ):
        findings.append(CompositionSignalFinding.LOW_TEXT_DENSITY_FOR_ROLE)
    required_groups = {
        VisualRoleExpectation.IMAGE_WITH_TAKEAWAYS: 2,
        VisualRoleExpectation.ACTION_FLOW: 3,
    }.get(signals.visual_role_expectation, 0)
    if signals.structured_visual_groups < required_groups:
        findings.append(CompositionSignalFinding.ROLE_STRUCTURE_MISSING)
    return tuple(findings)


@dataclass(frozen=True)
class EffectiveDensitySignals:
    """Countable structure supplied to semantic-depth review, not an aesthetic score."""

    card_count: int
    label_only_card_count: int
    supporting_card_count: int
    substantive_card_count: int
    distinct_informational_images: int
    related_detail_images: int
    duplicative_images: int
    decorative_images: int
    semantic_unit_count: int
    hierarchy_levels: int
    visual_role_expectation: VisualRoleExpectation
    has_role_supporting_layer: bool

    def __post_init__(self) -> None:
        counts = (
            self.card_count,
            self.label_only_card_count,
            self.supporting_card_count,
            self.substantive_card_count,
            self.distinct_informational_images,
            self.related_detail_images,
            self.duplicative_images,
            self.decorative_images,
            self.semantic_unit_count,
            self.hierarchy_levels,
        )
        if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in counts):
            raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
        if self.label_only_card_count + self.supporting_card_count + self.substantive_card_count != self.card_count:
            raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
        if not isinstance(self.visual_role_expectation, VisualRoleExpectation):
            raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
        if not isinstance(self.has_role_supporting_layer, bool):
            raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)


@dataclass(frozen=True)
class EffectiveDensityAssessment:
    """Reviewed bounded classifications attached to one exact rendered artifact."""

    slide_id: str
    artifact_sha256: str
    card_information_depth: CardInformationDepth
    image_variety: ImageVariety
    semantic_density: SemanticDensity
    signals: EffectiveDensitySignals
    rationale: str

    def __post_init__(self) -> None:
        if not re.fullmatch(r"slide_\d+", self.slide_id or ""):
            raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
        object.__setattr__(self, "artifact_sha256", _sha(self.artifact_sha256))
        if (
            not isinstance(self.card_information_depth, CardInformationDepth)
            or not isinstance(self.image_variety, ImageVariety)
            or not isinstance(self.semantic_density, SemanticDensity)
            or not isinstance(self.signals, EffectiveDensitySignals)
            or not isinstance(self.rationale, str)
            or not self.rationale.strip()
        ):
            raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)


def effective_density_signal_findings(
    signals: EffectiveDensitySignals,
) -> tuple[EffectiveDensitySignalFinding, ...]:
    """Return structural prompts without deriving semantic quality from raw density."""
    if not isinstance(signals, EffectiveDensitySignals):
        raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
    findings: list[EffectiveDensitySignalFinding] = []
    is_content_slide = signals.visual_role_expectation is not VisualRoleExpectation.COVER_HERO
    if is_content_slide and signals.label_only_card_count:
        findings.append(EffectiveDensitySignalFinding.LABEL_ONLY_CARD_PRESENT)
    if is_content_slide and signals.card_count and not (
        signals.supporting_card_count or signals.substantive_card_count
    ):
        findings.append(EffectiveDensitySignalFinding.CARD_SUPPORTING_LAYER_MISSING)
    if signals.duplicative_images:
        findings.append(EffectiveDensitySignalFinding.DUPLICATIVE_IMAGE_PRESENT)
    if signals.decorative_images:
        findings.append(EffectiveDensitySignalFinding.DECORATIVE_IMAGE_PRESENT)
    image_count = (
        signals.distinct_informational_images
        + signals.related_detail_images
        + signals.duplicative_images
        + signals.decorative_images
    )
    if image_count > 1 and not (
        signals.distinct_informational_images or signals.related_detail_images
    ):
        findings.append(EffectiveDensitySignalFinding.IMAGE_VARIETY_MISSING)
    if is_content_slide and not signals.has_role_supporting_layer:
        findings.append(EffectiveDensitySignalFinding.ROLE_SUPPORTING_LAYER_MISSING)
    return tuple(findings)


@dataclass(frozen=True)
class VisualObservation:
    """Deterministic facts extracted from an inspected comparison."""

    issue: VisualIssue
    semantic_content_changed: bool = False
    core_content_obscured: bool = False
    approved_quality_floor_violated: bool = False
    bounded_harmless_drift: bool = False
    repairable_degradation: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.issue, VisualIssue):
            raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
        flags = (
            self.semantic_content_changed,
            self.core_content_obscured,
            self.approved_quality_floor_violated,
            self.bounded_harmless_drift,
            self.repairable_degradation,
        )
        if any(not isinstance(item, bool) for item in flags):
            raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
        if self.bounded_harmless_drift and any(flags[:3]):
            raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)


def disposition_from_observation(observation: VisualObservation) -> VisualDisposition:
    """Apply the repository priority order to already-observed exact facts."""
    if not isinstance(observation, VisualObservation):
        raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
    if (
        observation.semantic_content_changed
        or observation.core_content_obscured
        or observation.approved_quality_floor_violated
    ):
        return VisualDisposition.BLOCK
    if observation.bounded_harmless_drift:
        return VisualDisposition.ACCEPT
    if observation.repairable_degradation:
        return VisualDisposition.REPAIR
    return VisualDisposition.WARNING


_DISPOSITION_ORDER = {
    VisualDisposition.ACCEPT: 0,
    VisualDisposition.WARNING: 1,
    VisualDisposition.REPAIR: 2,
    VisualDisposition.BLOCK: 3,
}
_STAGE_ORDER = {
    VisualStage.RAW_PLATE: 0,
    VisualStage.HYBRID_PREVIEW: 1,
    VisualStage.ACTUAL_CLIENT_RENDER: 2,
}


def _sha(value: str) -> str:
    clean = value.strip() if isinstance(value, str) else ""
    if not re.fullmatch(r"[0-9a-f]{64}", clean):
        raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
    return clean


@dataclass(frozen=True)
class RenderArtifactEvidence:
    slide_id: str
    stage: VisualStage
    artifact_sha256: str
    source_presentation_sha256: str
    environment: str
    actual_client: bool = False

    def __post_init__(self) -> None:
        if not re.fullmatch(r"slide_\d+", self.slide_id or ""):
            raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
        if not isinstance(self.stage, VisualStage) or not isinstance(self.actual_client, bool):
            raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
        object.__setattr__(self, "artifact_sha256", _sha(self.artifact_sha256))
        object.__setattr__(self, "source_presentation_sha256", _sha(self.source_presentation_sha256))
        environment = self.environment.strip() if isinstance(self.environment, str) else ""
        if not environment:
            raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
        if self.stage is VisualStage.ACTUAL_CLIENT_RENDER and not self.actual_client:
            raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
        if self.stage is not VisualStage.ACTUAL_CLIENT_RENDER and self.actual_client:
            raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
        object.__setattr__(self, "environment", environment)


@dataclass(frozen=True)
class StageComparison:
    slide_id: str
    reference_stage: VisualStage
    delivered_stage: VisualStage
    reference_sha256: str
    delivered_sha256: str
    degradation: MaterialDegradation
    issue: VisualIssue
    disposition: VisualDisposition
    detail: str

    def __post_init__(self) -> None:
        if not re.fullmatch(r"slide_\d+", self.slide_id or ""):
            raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
        if not all(isinstance(item, expected) for item, expected in (
            (self.reference_stage, VisualStage),
            (self.delivered_stage, VisualStage),
            (self.degradation, MaterialDegradation),
            (self.issue, VisualIssue),
            (self.disposition, VisualDisposition),
        )):
            raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
        if _STAGE_ORDER[self.delivered_stage] <= _STAGE_ORDER[self.reference_stage]:
            raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
        object.__setattr__(self, "reference_sha256", _sha(self.reference_sha256))
        object.__setattr__(self, "delivered_sha256", _sha(self.delivered_sha256))
        if not isinstance(self.detail, str) or not self.detail.strip():
            raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)


@dataclass(frozen=True)
class VisualQualificationReport:
    disposition: VisualDisposition
    comparisons: tuple[StageComparison, ...]
    earliest_material_loss: VisualStage | None
    actual_client_environment: str
    automated_human_gate: HumanPresentationQualityRecord

    @property
    def requires_human_review(self) -> bool:
        return True


def _validate_sample(sample: SampleArtifact, hybrid: RenderArtifactEvidence) -> None:
    if not isinstance(sample, SampleArtifact):
        raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
    provenance = sample.provenance or {}
    if provenance.get("artifact_kind") != "HYBRID_PREVIEW":
        raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
    if provenance.get("rendered_preview_sha256") != hybrid.artifact_sha256:
        raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)


def qualify_visual_pipeline(
    artifacts: Iterable[RenderArtifactEvidence],
    comparisons: Iterable[StageComparison],
    *,
    approved_sample: SampleArtifact,
) -> VisualQualificationReport:
    evidence = tuple(artifacts)
    checks = tuple(comparisons)
    if len(evidence) != 3 or any(not isinstance(item, RenderArtifactEvidence) for item in evidence):
        raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
    by_stage = {item.stage: item for item in evidence}
    if set(by_stage) != set(VisualStage):
        raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
    slide_ids = {item.slide_id for item in evidence}
    if len(slide_ids) != 1:
        raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
    hybrid = by_stage[VisualStage.HYBRID_PREVIEW]
    actual = by_stage[VisualStage.ACTUAL_CLIENT_RENDER]
    _validate_sample(approved_sample, hybrid)
    if not checks or any(not isinstance(item, StageComparison) for item in checks):
        raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
    required_edges = {
        (VisualStage.RAW_PLATE, VisualStage.HYBRID_PREVIEW),
        (VisualStage.HYBRID_PREVIEW, VisualStage.ACTUAL_CLIENT_RENDER),
    }
    if {(item.reference_stage, item.delivered_stage) for item in checks} != required_edges:
        raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
    evidence_hashes = {(item.stage, item.artifact_sha256) for item in evidence}
    for check in checks:
        if check.slide_id not in slide_ids:
            raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
        if (check.reference_stage, check.reference_sha256) not in evidence_hashes:
            raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
        if (check.delivered_stage, check.delivered_sha256) not in evidence_hashes:
            raise ValueError(ERROR_VISUAL_QUALIFICATION_INVALID)
    disposition = max(
        (item.disposition for item in checks),
        key=lambda item: _DISPOSITION_ORDER[item],
    )
    material = [
        item for item in checks
        if item.degradation in {MaterialDegradation.MATERIAL_DEGRADATION, MaterialDegradation.UNACCEPTABLE}
    ]
    earliest = min(
        (item.delivered_stage for item in material),
        key=lambda item: _STAGE_ORDER[item],
        default=None,
    )
    blocking = disposition is VisualDisposition.BLOCK
    automated_gate = automated_quality_assistance(
        actual.source_presentation_sha256,
        blocking=blocking,
        detail=(
            "Automated visual qualification found a blocking exact-artifact defect."
            if blocking
            else "Automated visual qualification completed; exact-artifact human acceptance is still required."
        ),
    )
    return VisualQualificationReport(
        disposition,
        checks,
        earliest,
        actual.environment,
        automated_gate,
    )


__all__ = [
    "CardInformationDepth",
    "CompositionAssessment",
    "CompositionDensity",
    "CompositionSignalFinding",
    "CompositionSignals",
    "EffectiveDensityAssessment",
    "EffectiveDensitySignalFinding",
    "EffectiveDensitySignals",
    "ERROR_VISUAL_QUALIFICATION_INVALID",
    "MaterialDegradation",
    "ImageVariety",
    "OccupiedContentEnvelope",
    "RenderArtifactEvidence",
    "SemanticDensity",
    "StageComparison",
    "TextDensitySignal",
    "VisualDisposition",
    "VisualAnchor",
    "VisualIssue",
    "VisualObservation",
    "VisualQualificationReport",
    "VisualRoleExpectation",
    "VisualStage",
    "composition_signal_findings",
    "disposition_from_observation",
    "effective_density_signal_findings",
    "qualify_visual_pipeline",
]
