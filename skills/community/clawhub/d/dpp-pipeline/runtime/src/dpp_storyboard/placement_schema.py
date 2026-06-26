from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .material import MaterialConfig
from .schema import StoryboardReport, StoryboardSegment


class PlacementAssessmentDraft(BaseModel):
    model_config = ConfigDict(extra="forbid")

    segment_index: int = Field(ge=1)
    suitability_score: float = Field(ge=0, le=10)
    decision: Literal["recommended", "possible", "avoid"]
    rationale: str = Field(min_length=1)
    suggested_placement: str
    concerns: list[str] = Field(default_factory=list)

    @field_validator("rationale", mode="before")
    @classmethod
    def _normalize_text(cls, value: Any) -> str:
        if not isinstance(value, str):
            raise TypeError("Expected a string.")
        normalized = value.strip()
        if not normalized:
            raise ValueError("Text fields cannot be empty.")
        return normalized

    @field_validator("suggested_placement", mode="before")
    @classmethod
    def _normalize_suggested_placement(cls, value: Any) -> str:
        if not isinstance(value, str):
            raise TypeError("Expected a string.")
        return value.strip()

    @field_validator("concerns", mode="before")
    @classmethod
    def _normalize_concerns(cls, value: Any) -> list[str]:
        if value is None:
            return []
        if not isinstance(value, list):
            raise TypeError("concerns must be a list of strings.")
        normalized: list[str] = []
        for item in value:
            if not isinstance(item, str):
                raise TypeError("concerns must be a list of strings.")
            stripped = item.strip()
            if stripped:
                normalized.append(stripped)
        return normalized

    @model_validator(mode="after")
    def _normalize_avoid_placement(self) -> "PlacementAssessmentDraft":
        if self.suggested_placement:
            return self
        if self.decision == "avoid":
            self.suggested_placement = "无明显可用植入空间"
            return self
        raise ValueError("suggested_placement cannot be empty unless decision is avoid.")


class BestPlacementSelectionDraft(BaseModel):
    model_config = ConfigDict(extra="forbid")

    best_segment_index: int = Field(ge=1)
    best_segment_reason: str = Field(min_length=1)

    @field_validator("best_segment_reason", mode="before")
    @classmethod
    def _normalize_reason(cls, value: Any) -> str:
        if not isinstance(value, str):
            raise TypeError("Expected a string.")
        normalized = value.strip()
        if not normalized:
            raise ValueError("best_segment_reason cannot be empty.")
        return normalized


class PlacementAnalysisDraft(BestPlacementSelectionDraft):
    model_config = ConfigDict(extra="forbid")

    assessments: list[PlacementAssessmentDraft] = Field(min_length=1)


class PlacementCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    segment_index: int = Field(ge=1)
    start_sec: float = Field(ge=0)
    end_sec: float = Field(gt=0)
    duration_sec: float = Field(gt=0)
    scene_summary: str = Field(min_length=1)
    background_summary: str | None = None
    spatial_layout: str | None = None
    lighting: str | None = None
    placement_space_hint: str | None = None
    thumbnail_path: str | None = None
    suitability_score: float = Field(ge=0, le=10)
    decision: Literal["recommended", "possible", "avoid"]
    rationale: str = Field(min_length=1)
    suggested_placement: str = Field(min_length=1)
    concerns: list[str] = Field(default_factory=list)


class PlacementAnalysisReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    storyboard_path: str = Field(min_length=1)
    material_brand: str = Field(min_length=1)
    material_product_name: str = Field(min_length=1)
    material_image_path: str = Field(min_length=1)
    model: str = Field(min_length=1)
    generated_at: str = Field(min_length=1)
    best_segment_index: int = Field(ge=1)
    best_segment_reason: str = Field(min_length=1)
    recommended_segment_indices: list[int] = Field(default_factory=list)
    candidates: list[PlacementCandidate] = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_candidates(self) -> "PlacementAnalysisReport":
        known_indices = {candidate.segment_index for candidate in self.candidates}
        if self.best_segment_index not in known_indices:
            raise ValueError(f"best_segment_index is not present in candidates: {self.best_segment_index}")
        if self.recommended_segment_indices:
            missing = [index for index in self.recommended_segment_indices if index not in known_indices]
            if missing:
                raise ValueError(f"recommended_segment_indices contains unknown segments: {missing}")
        return self


def build_placement_candidates(
    *,
    storyboard: StoryboardReport,
    assessments: list[PlacementAssessmentDraft],
) -> list[PlacementCandidate]:
    segment_map: dict[int, StoryboardSegment] = {segment.index: segment for segment in storyboard.segments}
    candidates = [
        PlacementCandidate(
            segment_index=assessment.segment_index,
            start_sec=segment_map[assessment.segment_index].start_sec,
            end_sec=segment_map[assessment.segment_index].end_sec,
            duration_sec=segment_map[assessment.segment_index].duration_sec,
            scene_summary=segment_map[assessment.segment_index].scene_summary,
            background_summary=segment_map[assessment.segment_index].background_summary,
            spatial_layout=segment_map[assessment.segment_index].spatial_layout,
            lighting=segment_map[assessment.segment_index].lighting,
            placement_space_hint=segment_map[assessment.segment_index].placement_space_hint,
            thumbnail_path=segment_map[assessment.segment_index].thumbnail_path,
            suitability_score=assessment.suitability_score,
            decision=assessment.decision,
            rationale=assessment.rationale,
            suggested_placement=assessment.suggested_placement,
            concerns=assessment.concerns,
        )
        for assessment in assessments
    ]
    candidates.sort(key=lambda item: (-item.suitability_score, item.segment_index))
    return candidates


def build_placement_analysis_report(
    *,
    storyboard_path: str,
    material: MaterialConfig,
    material_image_path: str,
    model: str,
    candidates: list[PlacementCandidate],
    best_segment_index: int,
    best_segment_reason: str,
    generated_at: str | None = None,
) -> PlacementAnalysisReport:
    recommended_segment_indices = [
        candidate.segment_index
        for candidate in candidates
        if candidate.decision == "recommended"
    ]
    timestamp = generated_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return PlacementAnalysisReport(
        storyboard_path=storyboard_path,
        material_brand=material.brand,
        material_product_name=material.product_name,
        material_image_path=material_image_path,
        model=model,
        generated_at=timestamp,
        best_segment_index=best_segment_index,
        best_segment_reason=best_segment_reason,
        recommended_segment_indices=recommended_segment_indices,
        candidates=candidates,
    )
