from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .material import MaterialConfig
from .placement_schema import PlacementAnalysisReport, PlacementCandidate
from .schema import StoryboardReport, StoryboardSegment


class CompositionPromptDraft(BaseModel):
    model_config = ConfigDict(extra="forbid")

    segment_index: int = Field(ge=1)
    scene_context: str = Field(min_length=1)
    product_feature_specs: str = Field(min_length=1)
    product_integration: str = Field(min_length=1)
    lighting: str = Field(min_length=1)
    motion: str = Field(min_length=1)
    mood: str = Field(min_length=1)
    negative_prompts: list[str] = Field(default_factory=list, min_length=1)
    generation_prompt: str = Field(min_length=1)

    @field_validator(
        "scene_context",
        "product_feature_specs",
        "product_integration",
        "lighting",
        "motion",
        "mood",
        "generation_prompt",
        mode="before",
    )
    @classmethod
    def _normalize_text(cls, value: Any) -> str:
        if not isinstance(value, str):
            raise TypeError("Expected a string.")
        normalized = value.strip()
        if not normalized:
            raise ValueError("Text fields cannot be empty.")
        return normalized

    @field_validator("negative_prompts", mode="before")
    @classmethod
    def _normalize_negative_prompts(cls, value: Any) -> list[str]:
        if value is None:
            return []
        if not isinstance(value, list):
            raise TypeError("negative_prompts must be a list of strings.")
        normalized: list[str] = []
        for item in value:
            if not isinstance(item, str):
                raise TypeError("negative_prompts must be a list of strings.")
            stripped = item.strip()
            if stripped:
                normalized.append(stripped)
        if not normalized:
            raise ValueError("negative_prompts cannot be empty.")
        return normalized


class BestSegmentReference(BaseModel):
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
    suggested_placement: str = Field(min_length=1)
    rationale: str = Field(min_length=1)
    concerns: list[str] = Field(default_factory=list)
    thumbnail_path: str = Field(min_length=1)
    reference_video_path: str = Field(min_length=1)
    reference_start_sec: float = Field(ge=0)
    reference_end_sec: float = Field(gt=0)

    @model_validator(mode="after")
    def _validate_duration(self) -> "BestSegmentReference":
        if self.end_sec <= self.start_sec:
            raise ValueError("end_sec must be greater than start_sec.")
        expected_duration = self.end_sec - self.start_sec
        if abs(self.duration_sec - expected_duration) > 1e-6:
            raise ValueError("duration_sec must equal end_sec - start_sec.")
        if self.reference_end_sec <= self.reference_start_sec:
            raise ValueError("reference_end_sec must be greater than reference_start_sec.")
        return self


class VideoGenerationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str = Field(min_length=1)
    status: str = Field(min_length=1)
    video_url: str | None = None
    downloaded_video_path: str | None = None
    last_frame_url: str | None = None
    file_url: str | None = None
    error_code: str | None = None
    error_message: str | None = None


class CompositionResultReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    storyboard_path: str = Field(min_length=1)
    placement_analysis_path: str = Field(min_length=1)
    material_brand: str = Field(min_length=1)
    material_product_name: str = Field(min_length=1)
    material_image_path: str = Field(min_length=1)
    prompt_model: str = Field(min_length=1)
    generation_model: str = Field(min_length=1)
    generated_at: str = Field(min_length=1)
    best_segment: BestSegmentReference
    prompt_plan: CompositionPromptDraft
    generation: VideoGenerationResult

    @model_validator(mode="after")
    def _validate_alignment(self) -> "CompositionResultReport":
        if self.best_segment.segment_index != self.prompt_plan.segment_index:
            raise ValueError("best_segment.segment_index must equal prompt_plan.segment_index.")
        if self.best_segment.segment_index < 1:
            raise ValueError("best_segment.segment_index must be positive.")
        return self


def build_best_segment_reference(
    *,
    storyboard: StoryboardReport,
    placement_analysis: PlacementAnalysisReport,
    thumbnail_path: str,
    reference_video_path: str,
    reference_start_sec: float,
    reference_end_sec: float,
) -> BestSegmentReference:
    segment_map: dict[int, StoryboardSegment] = {segment.index: segment for segment in storyboard.segments}
    candidate_map: dict[int, PlacementCandidate] = {
        candidate.segment_index: candidate for candidate in placement_analysis.candidates
    }
    best_segment_index = placement_analysis.best_segment_index
    if best_segment_index not in segment_map:
        raise ValueError(f"best_segment_index not found in storyboard: {best_segment_index}")
    if best_segment_index not in candidate_map:
        raise ValueError(f"best_segment_index not found in placement analysis candidates: {best_segment_index}")

    segment = segment_map[best_segment_index]
    candidate = candidate_map[best_segment_index]
    return BestSegmentReference(
        segment_index=segment.index,
        start_sec=segment.start_sec,
        end_sec=segment.end_sec,
        duration_sec=segment.duration_sec,
        scene_summary=segment.scene_summary,
        background_summary=segment.background_summary,
        spatial_layout=segment.spatial_layout,
        lighting=segment.lighting,
        placement_space_hint=segment.placement_space_hint,
        suggested_placement=candidate.suggested_placement,
        rationale=candidate.rationale,
        concerns=candidate.concerns,
        thumbnail_path=thumbnail_path,
        reference_video_path=reference_video_path,
        reference_start_sec=reference_start_sec,
        reference_end_sec=reference_end_sec,
    )


def build_composition_result_report(
    *,
    storyboard_path: str,
    placement_analysis_path: str,
    material: MaterialConfig,
    material_image_path: str,
    prompt_model: str,
    generation_model: str,
    best_segment: BestSegmentReference,
    prompt_plan: CompositionPromptDraft,
    generation: VideoGenerationResult,
    generated_at: str | None = None,
) -> CompositionResultReport:
    timestamp = generated_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return CompositionResultReport(
        storyboard_path=storyboard_path,
        placement_analysis_path=placement_analysis_path,
        material_brand=material.brand,
        material_product_name=material.product_name,
        material_image_path=material_image_path,
        prompt_model=prompt_model,
        generation_model=generation_model,
        generated_at=timestamp,
        best_segment=best_segment,
        prompt_plan=prompt_plan,
        generation=generation,
    )
