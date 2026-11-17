#!/usr/bin/env python3
"""Phase 18.2 deterministic element-level production planning."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from phase18_contract import (
    CropBehavior,
    DeliveryEditabilityContract,
    DeliveryProfile,
    EditabilityClass,
    EditabilityEnvelope,
    ElementBox,
    FontPortability,
    OverflowBehavior,
    PlateProvenanceMode,
    PlateRequirement,
    ProductionStrategy,
    ReplacementMode,
    ReplacementSemantics,
    ReservedEditableZone,
    ShrinkPolicy,
)


ERROR_PRODUCTION_PLAN_INVALID = "PHASE18_PRODUCTION_PLAN_INVALID"


class ProductionPlanError(Exception):
    def __init__(self, error_code: str, message: str) -> None:
        super().__init__(message)
        self.error_code = error_code


class ElementRole(str, Enum):
    NAME = "NAME"
    JOB_TITLE = "JOB_TITLE"
    DATE = "DATE"
    PRICE = "PRICE"
    KPI = "KPI"
    CONTACT = "CONTACT"
    CTA = "CTA"
    TITLE = "TITLE"
    BODY = "BODY"
    TABLE = "TABLE"
    LOGO = "LOGO"
    PHOTO = "PHOTO"
    SIMPLE_SHAPE = "SIMPLE_SHAPE"
    ARTISTIC_HEADLINE = "ARTISTIC_HEADLINE"
    HERO_ARTWORK = "HERO_ARTWORK"
    CHART = "CHART"
    DECORATIVE_ARTWORK = "DECORATIVE_ARTWORK"


class PortabilityRisk(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


_REQUIRED_TEXT = frozenset({
    ElementRole.NAME, ElementRole.JOB_TITLE, ElementRole.DATE, ElementRole.PRICE,
    ElementRole.KPI, ElementRole.CONTACT, ElementRole.CTA,
})
_TEXT = _REQUIRED_TEXT | frozenset({ElementRole.TITLE, ElementRole.BODY, ElementRole.TABLE})


def _clean(value: str, label: str) -> str:
    result = value.strip() if isinstance(value, str) else ""
    if not result:
        raise ProductionPlanError(ERROR_PRODUCTION_PLAN_INVALID, f"{label} is required")
    return result


@dataclass(frozen=True)
class ElementPlanningInput:
    element_id: str
    semantic_ref: str
    narrative_ref: str
    role: ElementRole
    approved_content: str
    font_portability: FontPortability = FontPortability.FONT_SAFE
    evidence_claim_ids: tuple[str, ...] = ()
    vector_safe: bool = False
    structured_data: bool = False

    def __post_init__(self) -> None:
        for name in ("element_id", "semantic_ref", "narrative_ref", "approved_content"):
            object.__setattr__(self, name, _clean(getattr(self, name), name))
        if not isinstance(self.role, ElementRole) or not isinstance(self.font_portability, FontPortability):
            raise ProductionPlanError(ERROR_PRODUCTION_PLAN_INVALID, "element role or font portability is invalid")
        if not isinstance(self.vector_safe, bool) or not isinstance(self.structured_data, bool):
            raise ProductionPlanError(ERROR_PRODUCTION_PLAN_INVALID, "planning flags must be boolean")
        claims = tuple(_clean(item, "evidence claim id") for item in self.evidence_claim_ids)
        if len(claims) != len(set(claims)):
            raise ProductionPlanError(ERROR_PRODUCTION_PLAN_INVALID, "evidence claim ids must be unique")
        object.__setattr__(self, "evidence_claim_ids", tuple(sorted(claims)))


@dataclass(frozen=True)
class ElementProductionPlan:
    plan_id: str
    element_id: str
    semantic_ref: str
    narrative_ref: str
    approved_content: str
    evidence_claim_ids: tuple[str, ...]
    role: ElementRole
    portability_risk: PortabilityRisk
    contract: DeliveryEditabilityContract

    def internal_dict(self) -> dict[str, object]:
        return {
            "plan_id": self.plan_id,
            "element_id": self.element_id,
            "semantic_ref": self.semantic_ref,
            "narrative_ref": self.narrative_ref,
            "approved_content": self.approved_content,
            "evidence_claim_ids": list(self.evidence_claim_ids),
            "role": self.role.value,
            "portability_risk": self.portability_risk.value,
            "contract": self.contract.internal_dict(),
        }

    def canonical_json(self) -> str:
        return json.dumps(self.internal_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _text_contract(item: ElementPlanningInput, profile: DeliveryProfile) -> tuple[DeliveryEditabilityContract, PortabilityRisk]:
    required = item.role in _REQUIRED_TEXT
    if item.font_portability is FontPortability.FONT_CRITICAL:
        editability = EditabilityClass.LOCKED_REQUIRED if item.role is ElementRole.ARTISTIC_HEADLINE else EditabilityClass.LOCKED_PREFERRED
        return DeliveryEditabilityContract(
            editability, ProductionStrategy.LOCKED_VISUAL, item.font_portability,
            delivery_profile=profile,
        ), PortabilityRisk.HIGH
    envelope_policy = {
        ElementRole.KPI: (16, 1, 24, 48),
        ElementRole.PRICE: (20, 1, 22, 44),
        ElementRole.DATE: (32, 2, 12, 24),
        ElementRole.CTA: (40, 2, 14, 28),
        ElementRole.NAME: (36, 2, 14, 40),
        ElementRole.JOB_TITLE: (48, 2, 12, 28),
        ElementRole.CONTACT: (96, 4, 10, 22),
        ElementRole.TITLE: (48, 2, 18, 40),
        ElementRole.TABLE: (240, 12, 9, 18),
        ElementRole.BODY: (180, 8, 10, 24),
    }
    max_chars, max_lines, minimum_font_size, maximum_font_size = envelope_policy[item.role]
    envelope = EditabilityEnvelope(
        expected_min_characters=1,
        expected_max_characters=max_chars,
        expected_min_lines=1,
        expected_max_lines=max_lines,
        minimum_font_size=minimum_font_size,
        maximum_font_size=maximum_font_size,
        shrink_policy=ShrinkPolicy.TO_MINIMUM,
        overflow_behavior=OverflowBehavior.FLAG_FOR_REVIEW,
        layout_tolerance_points=2.0,
    )
    return DeliveryEditabilityContract(
        EditabilityClass.EDITABLE_REQUIRED if required else EditabilityClass.EDITABLE_PREFERRED,
        ProductionStrategy.NATIVE_TEXT,
        item.font_portability,
        envelope=envelope,
        delivery_profile=profile,
    ), PortabilityRisk.LOW if item.font_portability is FontPortability.FONT_SAFE else PortabilityRisk.MEDIUM


def _replacement_contract(
    item: ElementPlanningInput,
    profile: DeliveryProfile,
    strategy: ProductionStrategy,
) -> DeliveryEditabilityContract:
    return DeliveryEditabilityContract(
        EditabilityClass.REPLACEABLE,
        strategy,
        item.font_portability,
        envelope=EditabilityEnvelope(
            replacement_min_aspect_ratio=0.5,
            replacement_max_aspect_ratio=2.5,
            crop_behavior=CropBehavior.PRESERVE_CROP if item.role is ElementRole.PHOTO else CropBehavior.PRESERVE_FRAME,
            layout_tolerance_points=1.0,
        ),
        replacement=ReplacementSemantics(
            ReplacementMode.PRESERVE_CROP if item.role is ElementRole.PHOTO else ReplacementMode.PRESERVE_FRAME
        ),
        delivery_profile=profile,
    )


def plan_element(item: ElementPlanningInput, profile: DeliveryProfile = DeliveryProfile.BALANCED) -> ElementProductionPlan:
    """Apply categorical policy; never alter approved content or semantic identities."""
    if not isinstance(item, ElementPlanningInput) or not isinstance(profile, DeliveryProfile):
        raise ProductionPlanError(ERROR_PRODUCTION_PLAN_INVALID, "element and delivery profile are required")
    if item.role in _TEXT:
        contract, risk = _text_contract(item, profile)
    elif item.role is ElementRole.ARTISTIC_HEADLINE:
        contract = DeliveryEditabilityContract(
            EditabilityClass.LOCKED_REQUIRED,
            ProductionStrategy.LOCKED_VISUAL,
            FontPortability.FONT_CRITICAL,
            delivery_profile=profile,
        )
        risk = PortabilityRisk.HIGH
    elif item.role in {ElementRole.LOGO, ElementRole.PHOTO}:
        strategy = ProductionStrategy.VECTOR_GRAPHIC if item.role is ElementRole.LOGO and item.vector_safe else ProductionStrategy.NATIVE_IMAGE
        contract = _replacement_contract(item, profile, strategy)
        risk = PortabilityRisk.LOW if strategy is ProductionStrategy.NATIVE_IMAGE else PortabilityRisk.MEDIUM
    elif item.role is ElementRole.SIMPLE_SHAPE:
        contract = DeliveryEditabilityContract(
            EditabilityClass.EDITABLE_PREFERRED,
            ProductionStrategy.NATIVE_SHAPE,
            item.font_portability,
            delivery_profile=profile,
        )
        risk = PortabilityRisk.LOW
    elif item.role is ElementRole.CHART:
        if item.structured_data:
            contract = DeliveryEditabilityContract(
                EditabilityClass.EDITABLE_PREFERRED,
                ProductionStrategy.NATIVE_CHART,
                item.font_portability,
                delivery_profile=profile,
            )
            risk = PortabilityRisk.MEDIUM
        else:
            contract = DeliveryEditabilityContract(
                EditabilityClass.LOCKED_PREFERRED,
                ProductionStrategy.RASTER_REGION,
                item.font_portability,
                delivery_profile=profile,
            )
            risk = PortabilityRisk.LOW
    else:
        if item.vector_safe and profile is DeliveryProfile.EDITABILITY_PRIORITY and item.role is ElementRole.DECORATIVE_ARTWORK:
            contract = DeliveryEditabilityContract(
                EditabilityClass.EDITABLE_PREFERRED,
                ProductionStrategy.VECTOR_GRAPHIC,
                item.font_portability,
                delivery_profile=profile,
            )
            risk = PortabilityRisk.MEDIUM
        else:
            contract = DeliveryEditabilityContract(
                EditabilityClass.LOCKED_REQUIRED if item.role is ElementRole.HERO_ARTWORK else EditabilityClass.LOCKED_PREFERRED,
                ProductionStrategy.LOCKED_VISUAL if profile is DeliveryProfile.FIDELITY else ProductionStrategy.RASTER_REGION,
                item.font_portability,
                delivery_profile=profile,
            )
            risk = PortabilityRisk.LOW
    payload = {
        "element_id": item.element_id,
        "semantic_ref": item.semantic_ref,
        "narrative_ref": item.narrative_ref,
        "approved_content": item.approved_content,
        "evidence_claim_ids": list(item.evidence_claim_ids),
        "role": item.role.value,
        "portability_risk": risk.value,
        "contract": contract.internal_dict(),
    }
    plan_id = "ep:" + hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    ).hexdigest()[:16]
    return ElementProductionPlan(
        plan_id, item.element_id, item.semantic_ref, item.narrative_ref, item.approved_content,
        item.evidence_claim_ids, item.role, risk, contract,
    )


def plan_elements(
    elements: Iterable[ElementPlanningInput],
    profile: DeliveryProfile = DeliveryProfile.BALANCED,
) -> tuple[ElementProductionPlan, ...]:
    clean = tuple(elements)
    if not clean or any(not isinstance(item, ElementPlanningInput) for item in clean):
        raise ProductionPlanError(ERROR_PRODUCTION_PLAN_INVALID, "elements are required")
    if len({item.element_id for item in clean}) != len(clean):
        raise ProductionPlanError(ERROR_PRODUCTION_PLAN_INVALID, "element ids must be unique")
    return tuple(plan_element(item, profile) for item in clean)


def derive_reserved_zone(
    plan: ElementProductionPlan,
    slide_id: str,
    box: ElementBox,
    background_treatment: str = "transparent",
) -> ReservedEditableZone:
    """Derive a deterministic reserved editable zone from an approved element plan."""
    if not isinstance(plan, ElementProductionPlan) or not isinstance(box, ElementBox):
        raise ProductionPlanError(ERROR_PRODUCTION_PLAN_INVALID, "plan and box are required")
    if not isinstance(slide_id, str) or not slide_id.strip():
        raise ProductionPlanError(ERROR_PRODUCTION_PLAN_INVALID, "slide_id is required")

    strategy = plan.contract.strategy
    if strategy is ProductionStrategy.NATIVE_TEXT:
        content_type = "text"
        plate_req = PlateRequirement.CONTENT_FREE
    elif strategy in {ProductionStrategy.NATIVE_IMAGE, ProductionStrategy.VECTOR_GRAPHIC}:
        content_type = "image"
        plate_req = PlateRequirement.CONTENT_FREE
    elif strategy is ProductionStrategy.NATIVE_CHART:
        content_type = "chart"
        plate_req = PlateRequirement.CONTENT_FREE
    elif strategy is ProductionStrategy.NATIVE_SHAPE:
        content_type = "shape"
        plate_req = (
            PlateRequirement.CONTENT_FREE
            if plan.contract.editability != EditabilityClass.LOCKED_REQUIRED
            else PlateRequirement.LOCKED_IN_PLATE
        )
    else:
        content_type = "visual"
        plate_req = PlateRequirement.LOCKED_IN_PLATE

    return ReservedEditableZone(
        zone_id=f"zone:{slide_id}:{plan.element_id}",
        slide_id=slide_id,
        element_id=plan.element_id,
        role=plan.role.value,
        box=box,
        editability=plan.contract.editability,
        strategy=strategy,
        expected_content_type=content_type,
        plate_requirement=plate_req,
        replacement=plan.contract.replacement,
        envelope=plan.contract.envelope,
        background_treatment=background_treatment,
    )


@dataclass(frozen=True)
class VisualPlateJobSpec:
    slide_id: str
    plate_mode: PlateProvenanceMode
    reserved_zones: tuple[ReservedEditableZone, ...]
    locked_content_to_render: tuple[str, ...]
    editable_content_to_omit: tuple[str, ...]
    replaceable_assets_to_omit: tuple[str, ...]
    background_instructions: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.slide_id, str) or not self.slide_id.strip():
            raise ProductionPlanError(ERROR_PRODUCTION_PLAN_INVALID, "slide_id is required")
        if not isinstance(self.plate_mode, PlateProvenanceMode):
            raise ProductionPlanError(ERROR_PRODUCTION_PLAN_INVALID, "plate_mode is invalid")
        zones = tuple(self.reserved_zones)
        if any(not isinstance(z, ReservedEditableZone) for z in zones):
            raise ProductionPlanError(ERROR_PRODUCTION_PLAN_INVALID, "reserved_zones contains invalid zone")
        object.__setattr__(self, "reserved_zones", zones)
        object.__setattr__(self, "locked_content_to_render", tuple(self.locked_content_to_render))
        object.__setattr__(self, "editable_content_to_omit", tuple(self.editable_content_to_omit))
        object.__setattr__(self, "replaceable_assets_to_omit", tuple(self.replaceable_assets_to_omit))

    def internal_dict(self) -> dict[str, object]:
        return {
            "slide_id": self.slide_id,
            "plate_mode": self.plate_mode.value,
            "reserved_zones": [z.internal_dict() for z in self.reserved_zones],
            "locked_content_to_render": list(self.locked_content_to_render),
            "editable_content_to_omit": list(self.editable_content_to_omit),
            "replaceable_assets_to_omit": list(self.replaceable_assets_to_omit),
            "background_instructions": self.background_instructions,
        }

    def canonical_json(self) -> str:
        return json.dumps(self.internal_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def create_visual_plate_job(
    slide_id: str,
    plans_with_boxes: Iterable[tuple[ElementProductionPlan, ElementBox]],
    plate_mode: PlateProvenanceMode = PlateProvenanceMode.CLEAN_PLATE,
    background_instructions: str = "",
) -> VisualPlateJobSpec:
    """Create a deterministic visual plate job specification with clean-plate requirements."""
    pairs = tuple(plans_with_boxes)
    if not pairs or any(not isinstance(item, tuple) or len(item) != 2 for item in pairs):
        raise ProductionPlanError(ERROR_PRODUCTION_PLAN_INVALID, "plans_with_boxes must be pairs of plan and box")
    if not isinstance(plate_mode, PlateProvenanceMode):
        raise ProductionPlanError(ERROR_PRODUCTION_PLAN_INVALID, "plate_mode is invalid")

    locked_render: list[str] = []
    editable_omit: list[str] = []
    replaceable_omit: list[str] = []
    reserved_zones: list[ReservedEditableZone] = []

    for plan, box in pairs:
        if not isinstance(plan, ElementProductionPlan) or not isinstance(box, ElementBox):
            raise ProductionPlanError(ERROR_PRODUCTION_PLAN_INVALID, "invalid plan or box")

        if plate_mode is PlateProvenanceMode.FULL_COMPOSITE:
            locked_render.append(plan.approved_content)
        elif plate_mode is PlateProvenanceMode.CLEAN_PLATE:
            strategy = plan.contract.strategy
            if strategy in {ProductionStrategy.NATIVE_IMAGE, ProductionStrategy.VECTOR_GRAPHIC}:
                replaceable_omit.append(plan.approved_content)
                reserved_zones.append(derive_reserved_zone(plan, slide_id, box))
            elif strategy in {ProductionStrategy.NATIVE_TEXT, ProductionStrategy.NATIVE_CHART, ProductionStrategy.NATIVE_SHAPE}:
                editable_omit.append(plan.approved_content)
                reserved_zones.append(derive_reserved_zone(plan, slide_id, box))
            else:
                locked_render.append(plan.approved_content)
        elif plate_mode is PlateProvenanceMode.PARTIAL_COMPOSITE:
            if (
                plan.contract.editability in {EditabilityClass.LOCKED_REQUIRED, EditabilityClass.LOCKED_PREFERRED}
                or plan.contract.strategy in {ProductionStrategy.LOCKED_VISUAL, ProductionStrategy.RASTER_REGION, ProductionStrategy.FULL_RASTER_SLIDE}
            ):
                locked_render.append(plan.approved_content)
            else:
                strategy = plan.contract.strategy
                if strategy in {ProductionStrategy.NATIVE_IMAGE, ProductionStrategy.VECTOR_GRAPHIC}:
                    replaceable_omit.append(plan.approved_content)
                else:
                    editable_omit.append(plan.approved_content)
                reserved_zones.append(derive_reserved_zone(plan, slide_id, box))

    return VisualPlateJobSpec(
        slide_id=slide_id,
        plate_mode=plate_mode,
        reserved_zones=tuple(reserved_zones),
        locked_content_to_render=tuple(locked_render),
        editable_content_to_omit=tuple(editable_omit),
        replaceable_assets_to_omit=tuple(replaceable_omit),
        background_instructions=background_instructions,
    )


__all__ = [
    "ERROR_PRODUCTION_PLAN_INVALID", "ElementPlanningInput", "ElementProductionPlan",
    "ElementRole", "PortabilityRisk", "ProductionPlanError", "VisualPlateJobSpec",
    "create_visual_plate_job", "derive_reserved_zone", "plan_element", "plan_elements",
]
