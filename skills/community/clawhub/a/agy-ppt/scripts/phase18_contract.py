#!/usr/bin/env python3
"""Phase 18.1 deterministic delivery and editability contracts."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from enum import Enum


ERROR_EDITABILITY_CONTRACT_INVALID = "PHASE18_EDITABILITY_CONTRACT_INVALID"


class EditabilityContractError(Exception):
    def __init__(self, error_code: str, message: str) -> None:
        super().__init__(message)
        self.error_code = error_code


class EditabilityClass(str, Enum):
    EDITABLE_REQUIRED = "EDITABLE_REQUIRED"
    EDITABLE_PREFERRED = "EDITABLE_PREFERRED"
    REPLACEABLE = "REPLACEABLE"
    LOCKED_PREFERRED = "LOCKED_PREFERRED"
    LOCKED_REQUIRED = "LOCKED_REQUIRED"


class ProductionStrategy(str, Enum):
    NATIVE_TEXT = "NATIVE_TEXT"
    NATIVE_SHAPE = "NATIVE_SHAPE"
    NATIVE_IMAGE = "NATIVE_IMAGE"
    NATIVE_CHART = "NATIVE_CHART"
    VECTOR_GRAPHIC = "VECTOR_GRAPHIC"
    RASTER_REGION = "RASTER_REGION"
    LOCKED_VISUAL = "LOCKED_VISUAL"
    FULL_RASTER_SLIDE = "FULL_RASTER_SLIDE"


class FontPortability(str, Enum):
    FONT_SAFE = "FONT_SAFE"
    FONT_FALLBACK_TOLERANT = "FONT_FALLBACK_TOLERANT"
    FONT_CRITICAL = "FONT_CRITICAL"


class DeliveryProfile(str, Enum):
    FIDELITY = "FIDELITY"
    BALANCED = "BALANCED"
    EDITABILITY_PRIORITY = "EDITABILITY_PRIORITY"


DEFAULT_DELIVERY_PROFILE = DeliveryProfile.BALANCED


class ShrinkPolicy(str, Enum):
    NEVER = "NEVER"
    TO_MINIMUM = "TO_MINIMUM"


class OverflowBehavior(str, Enum):
    FLAG_FOR_REVIEW = "FLAG_FOR_REVIEW"
    WRAP_WITHIN_ENVELOPE = "WRAP_WITHIN_ENVELOPE"
    LOCKED_FALLBACK = "LOCKED_FALLBACK"


class CropBehavior(str, Enum):
    NOT_APPLICABLE = "NOT_APPLICABLE"
    PRESERVE_FRAME = "PRESERVE_FRAME"
    PRESERVE_CROP = "PRESERVE_CROP"


class ReplacementMode(str, Enum):
    NOT_REPLACEABLE = "NOT_REPLACEABLE"
    PRESERVE_FRAME = "PRESERVE_FRAME"
    PRESERVE_CROP = "PRESERVE_CROP"
    WITHIN_ASPECT_ENVELOPE = "WITHIN_ASPECT_ENVELOPE"


def _optional_int(value: int | None, name: str, *, minimum: int = 0) -> None:
    if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value < minimum):
        raise EditabilityContractError(ERROR_EDITABILITY_CONTRACT_INVALID, f"{name} is invalid")


def _optional_number(value: float | None, name: str, *, minimum: float = 0.0) -> None:
    if value is not None and (
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not math.isfinite(float(value))
        or float(value) < minimum
    ):
        raise EditabilityContractError(ERROR_EDITABILITY_CONTRACT_INVALID, f"{name} is invalid")


@dataclass(frozen=True)
class EditabilityEnvelope:
    expected_min_characters: int | None = None
    expected_max_characters: int | None = None
    expected_min_lines: int | None = None
    expected_max_lines: int | None = None
    minimum_font_size: float | None = None
    maximum_font_size: float | None = None
    shrink_policy: ShrinkPolicy = ShrinkPolicy.NEVER
    overflow_behavior: OverflowBehavior = OverflowBehavior.FLAG_FOR_REVIEW
    replacement_min_aspect_ratio: float | None = None
    replacement_max_aspect_ratio: float | None = None
    crop_behavior: CropBehavior = CropBehavior.NOT_APPLICABLE
    layout_tolerance_points: float | None = None

    def __post_init__(self) -> None:
        for name in ("expected_min_characters", "expected_max_characters", "expected_min_lines", "expected_max_lines"):
            _optional_int(getattr(self, name), name)
        for name in (
            "minimum_font_size", "maximum_font_size", "replacement_min_aspect_ratio",
            "replacement_max_aspect_ratio", "layout_tolerance_points",
        ):
            _optional_number(getattr(self, name), name)
        if not isinstance(self.shrink_policy, ShrinkPolicy) or not isinstance(self.overflow_behavior, OverflowBehavior):
            raise EditabilityContractError(ERROR_EDITABILITY_CONTRACT_INVALID, "text behavior is invalid")
        if not isinstance(self.crop_behavior, CropBehavior):
            raise EditabilityContractError(ERROR_EDITABILITY_CONTRACT_INVALID, "crop behavior is invalid")
        pairs = (
            (self.expected_min_characters, self.expected_max_characters, "character range"),
            (self.expected_min_lines, self.expected_max_lines, "line range"),
            (self.minimum_font_size, self.maximum_font_size, "font-size range"),
            (self.replacement_min_aspect_ratio, self.replacement_max_aspect_ratio, "aspect-ratio range"),
        )
        for lower, upper, label in pairs:
            if lower is not None and upper is not None and lower > upper:
                raise EditabilityContractError(ERROR_EDITABILITY_CONTRACT_INVALID, f"{label} is inverted")
        if self.shrink_policy is ShrinkPolicy.TO_MINIMUM and self.minimum_font_size is None:
            raise EditabilityContractError(ERROR_EDITABILITY_CONTRACT_INVALID, "shrink policy requires a minimum font size")
        if self.crop_behavior is not CropBehavior.NOT_APPLICABLE and (
            self.replacement_min_aspect_ratio is None or self.replacement_max_aspect_ratio is None
        ):
            raise EditabilityContractError(ERROR_EDITABILITY_CONTRACT_INVALID, "crop behavior requires an aspect envelope")

    def internal_dict(self) -> dict[str, object]:
        return {
            "expected_min_characters": self.expected_min_characters,
            "expected_max_characters": self.expected_max_characters,
            "expected_min_lines": self.expected_min_lines,
            "expected_max_lines": self.expected_max_lines,
            "minimum_font_size": self.minimum_font_size,
            "maximum_font_size": self.maximum_font_size,
            "shrink_policy": self.shrink_policy.value,
            "overflow_behavior": self.overflow_behavior.value,
            "replacement_min_aspect_ratio": self.replacement_min_aspect_ratio,
            "replacement_max_aspect_ratio": self.replacement_max_aspect_ratio,
            "crop_behavior": self.crop_behavior.value,
            "layout_tolerance_points": self.layout_tolerance_points,
        }


@dataclass(frozen=True)
class ReplacementSemantics:
    mode: ReplacementMode = ReplacementMode.NOT_REPLACEABLE
    preserve_position: bool = True
    preserve_size: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.mode, ReplacementMode):
            raise EditabilityContractError(ERROR_EDITABILITY_CONTRACT_INVALID, "replacement mode is invalid")
        if not isinstance(self.preserve_position, bool) or not isinstance(self.preserve_size, bool):
            raise EditabilityContractError(ERROR_EDITABILITY_CONTRACT_INVALID, "replacement flags must be boolean")

    def internal_dict(self) -> dict[str, object]:
        return {
            "mode": self.mode.value,
            "preserve_position": self.preserve_position,
            "preserve_size": self.preserve_size,
        }


@dataclass(frozen=True)
class DeliveryEditabilityContract:
    editability: EditabilityClass
    strategy: ProductionStrategy
    font_portability: FontPortability
    envelope: EditabilityEnvelope | None = None
    replacement: ReplacementSemantics = ReplacementSemantics()
    delivery_profile: DeliveryProfile = DEFAULT_DELIVERY_PROFILE

    def __post_init__(self) -> None:
        if not isinstance(self.editability, EditabilityClass):
            raise EditabilityContractError(ERROR_EDITABILITY_CONTRACT_INVALID, "editability class is invalid")
        if not isinstance(self.strategy, ProductionStrategy):
            raise EditabilityContractError(ERROR_EDITABILITY_CONTRACT_INVALID, "production strategy is invalid")
        if not isinstance(self.font_portability, FontPortability):
            raise EditabilityContractError(ERROR_EDITABILITY_CONTRACT_INVALID, "font portability is invalid")
        if self.envelope is not None and not isinstance(self.envelope, EditabilityEnvelope):
            raise EditabilityContractError(ERROR_EDITABILITY_CONTRACT_INVALID, "editability envelope is invalid")
        if not isinstance(self.replacement, ReplacementSemantics) or not isinstance(self.delivery_profile, DeliveryProfile):
            raise EditabilityContractError(ERROR_EDITABILITY_CONTRACT_INVALID, "delivery contract metadata is invalid")
        if self.replacement.mode is not ReplacementMode.NOT_REPLACEABLE and self.editability is not EditabilityClass.REPLACEABLE:
            raise EditabilityContractError(ERROR_EDITABILITY_CONTRACT_INVALID, "replacement behavior requires REPLACEABLE editability")

    def internal_dict(self) -> dict[str, object]:
        return {
            "editability": self.editability.value,
            "production_strategy": self.strategy.value,
            "font_portability": self.font_portability.value,
            "editability_envelope": self.envelope.internal_dict() if self.envelope else None,
            "replacement": self.replacement.internal_dict(),
            "delivery_profile": self.delivery_profile.value,
        }

    def canonical_json(self) -> str:
        return json.dumps(self.internal_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


class PlateProvenanceMode(str, Enum):
    CLEAN_PLATE = "CLEAN_PLATE"
    PARTIAL_COMPOSITE = "PARTIAL_COMPOSITE"
    FULL_COMPOSITE = "FULL_COMPOSITE"


class PlateRequirement(str, Enum):
    CONTENT_FREE = "CONTENT_FREE"
    LOCKED_IN_PLATE = "LOCKED_IN_PLATE"


@dataclass(frozen=True)
class ElementBox:
    left: float
    top: float
    width: float
    height: float

    def __post_init__(self) -> None:
        values = (self.left, self.top, self.width, self.height)
        if any(not isinstance(value, (int, float)) or isinstance(value, bool) for value in values):
            raise EditabilityContractError(ERROR_EDITABILITY_CONTRACT_INVALID, "element box must use numeric inches")
        if self.left < 0 or self.top < 0 or self.width <= 0 or self.height <= 0:
            raise EditabilityContractError(ERROR_EDITABILITY_CONTRACT_INVALID, "element box is outside the slide")

    def internal_dict(self) -> dict[str, float]:
        return {
            "left": float(self.left),
            "top": float(self.top),
            "width": float(self.width),
            "height": float(self.height),
        }


@dataclass(frozen=True)
class ReservedEditableZone:
    zone_id: str
    slide_id: str
    element_id: str
    role: str
    box: ElementBox
    editability: EditabilityClass
    strategy: ProductionStrategy
    expected_content_type: str
    plate_requirement: PlateRequirement = PlateRequirement.CONTENT_FREE
    replacement: ReplacementSemantics = ReplacementSemantics()
    envelope: EditabilityEnvelope | None = None
    background_treatment: str = "transparent"

    def __post_init__(self) -> None:
        for name in ("zone_id", "slide_id", "element_id", "role", "background_treatment"):
            val = getattr(self, name)
            if not isinstance(val, str) or not val.strip():
                raise EditabilityContractError(ERROR_EDITABILITY_CONTRACT_INVALID, f"{name} must be a non-empty string")
        if not isinstance(self.box, ElementBox):
            raise EditabilityContractError(ERROR_EDITABILITY_CONTRACT_INVALID, "box must be an ElementBox")
        if not isinstance(self.editability, EditabilityClass):
            raise EditabilityContractError(ERROR_EDITABILITY_CONTRACT_INVALID, "editability must be an EditabilityClass")
        if not isinstance(self.strategy, ProductionStrategy):
            raise EditabilityContractError(ERROR_EDITABILITY_CONTRACT_INVALID, "strategy must be a ProductionStrategy")
        if self.expected_content_type not in {"text", "image", "chart", "shape", "visual"}:
            raise EditabilityContractError(ERROR_EDITABILITY_CONTRACT_INVALID, "expected_content_type is invalid")
        if not isinstance(self.plate_requirement, PlateRequirement):
            raise EditabilityContractError(ERROR_EDITABILITY_CONTRACT_INVALID, "plate_requirement must be a PlateRequirement")
        if not isinstance(self.replacement, ReplacementSemantics):
            raise EditabilityContractError(ERROR_EDITABILITY_CONTRACT_INVALID, "replacement must be a ReplacementSemantics")
        if self.envelope is not None and not isinstance(self.envelope, EditabilityEnvelope):
            raise EditabilityContractError(ERROR_EDITABILITY_CONTRACT_INVALID, "envelope must be an EditabilityEnvelope")

        # CONTENT-FREE INVARIANT:
        # Every NATIVE_TEXT, NATIVE_IMAGE, NATIVE_CHART that visually replaces semantic content
        # must require CONTENT_FREE plate provenance for its zone.
        if self.strategy in {
            ProductionStrategy.NATIVE_TEXT,
            ProductionStrategy.NATIVE_IMAGE,
            ProductionStrategy.NATIVE_CHART,
        } and self.editability in {
            EditabilityClass.EDITABLE_REQUIRED,
            EditabilityClass.EDITABLE_PREFERRED,
            EditabilityClass.REPLACEABLE,
        }:
            if self.plate_requirement is not PlateRequirement.CONTENT_FREE:
                raise EditabilityContractError(
                    ERROR_EDITABILITY_CONTRACT_INVALID,
                    "native editable objects require CONTENT_FREE plate requirement",
                )

    def internal_dict(self) -> dict[str, object]:
        return {
            "zone_id": self.zone_id,
            "slide_id": self.slide_id,
            "element_id": self.element_id,
            "role": self.role,
            "box": self.box.internal_dict(),
            "editability": self.editability.value,
            "strategy": self.strategy.value,
            "expected_content_type": self.expected_content_type,
            "plate_requirement": self.plate_requirement.value,
            "replacement": self.replacement.internal_dict(),
            "envelope": self.envelope.internal_dict() if self.envelope else None,
            "background_treatment": self.background_treatment,
        }

    def canonical_json(self) -> str:
        return json.dumps(self.internal_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def user_facing_delivery_message() -> str:
    return "我會在維持核准視覺品質的前提下，讓重要內容保有安全、實用的可修改性。"


__all__ = [
    "DEFAULT_DELIVERY_PROFILE", "ERROR_EDITABILITY_CONTRACT_INVALID", "CropBehavior",
    "DeliveryEditabilityContract", "DeliveryProfile", "EditabilityClass",
    "EditabilityContractError", "EditabilityEnvelope", "ElementBox", "FontPortability",
    "OverflowBehavior", "PlateProvenanceMode", "PlateRequirement", "ProductionStrategy",
    "ReplacementMode", "ReplacementSemantics", "ReservedEditableZone",
    "ShrinkPolicy", "user_facing_delivery_message",
]
