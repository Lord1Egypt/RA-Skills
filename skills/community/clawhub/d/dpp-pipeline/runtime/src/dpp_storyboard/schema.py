from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class StoryboardDraftSegment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    index: int = Field(ge=1)
    start_sec: float = Field(ge=0)
    end_sec: float = Field(gt=0)
    scene_summary: str = Field(min_length=1)
    background_summary: str | None = None
    spatial_layout: str | None = None
    lighting: str | None = None
    placement_space_hint: str | None = None
    characters: list[str] = Field(default_factory=list)
    actions: list[str] = Field(default_factory=list)
    camera_motion: str = Field(min_length=1)

    @field_validator("scene_summary", "camera_motion", mode="before")
    @classmethod
    def _normalize_text(cls, value: Any) -> str:
        if not isinstance(value, str):
            raise TypeError("Expected a string.")
        normalized = value.strip()
        if not normalized:
            raise ValueError("Text fields cannot be empty.")
        return normalized

    @field_validator(
        "background_summary",
        "spatial_layout",
        "lighting",
        "placement_space_hint",
        mode="before",
    )
    @classmethod
    def _normalize_optional_text(cls, value: Any) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str):
            raise TypeError("Expected a string.")
        normalized = value.strip()
        return normalized or None

    @field_validator("characters", "actions", mode="before")
    @classmethod
    def _normalize_lists(cls, value: Any) -> list[str]:
        if value is None:
            return []
        if not isinstance(value, list):
            raise TypeError("Expected a list of strings.")
        normalized: list[str] = []
        for item in value:
            if not isinstance(item, str):
                raise TypeError("Expected a list of strings.")
            stripped = item.strip()
            if stripped:
                normalized.append(stripped)
        return normalized

    @model_validator(mode="after")
    def _validate_times(self) -> "StoryboardDraftSegment":
        if self.end_sec <= self.start_sec:
            raise ValueError("end_sec must be greater than start_sec.")
        return self


class StoryboardDraft(BaseModel):
    model_config = ConfigDict(extra="forbid")

    language: str = Field(default="zh-CN", min_length=1)
    segments: list[StoryboardDraftSegment] = Field(min_length=1)

    @field_validator("language", mode="before")
    @classmethod
    def _normalize_language(cls, value: Any) -> str:
        if value is None:
            return "zh-CN"
        if not isinstance(value, str):
            raise TypeError("language must be a string.")
        normalized = value.strip()
        if not normalized:
            raise ValueError("language cannot be empty.")
        return normalized


class StoryboardSegment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    index: int = Field(ge=1)
    start_sec: float = Field(ge=0)
    end_sec: float = Field(gt=0)
    duration_sec: float = Field(gt=0)
    scene_summary: str = Field(min_length=1)
    background_summary: str | None = None
    spatial_layout: str | None = None
    lighting: str | None = None
    placement_space_hint: str | None = None
    characters: list[str] = Field(default_factory=list)
    actions: list[str] = Field(default_factory=list)
    camera_motion: str = Field(min_length=1)
    thumbnail_path: str | None = None

    @field_validator(
        "scene_summary",
        "camera_motion",
        "background_summary",
        "spatial_layout",
        "lighting",
        "placement_space_hint",
        mode="before",
    )
    @classmethod
    def _normalize_segment_text(cls, value: Any, info: Any) -> str | None:
        if value is None:
            if info.field_name in {"background_summary", "spatial_layout", "lighting", "placement_space_hint"}:
                return None
            raise TypeError("Expected a string.")
        if not isinstance(value, str):
            raise TypeError("Expected a string.")
        normalized = value.strip()
        if not normalized:
            if info.field_name in {"background_summary", "spatial_layout", "lighting", "placement_space_hint"}:
                return None
            raise ValueError("Text fields cannot be empty.")
        return normalized

    @model_validator(mode="after")
    def _validate_duration(self) -> "StoryboardSegment":
        expected = self.end_sec - self.start_sec
        if self.end_sec <= self.start_sec:
            raise ValueError("end_sec must be greater than start_sec.")
        if abs(self.duration_sec - expected) > 1e-6:
            raise ValueError("duration_sec must equal end_sec - start_sec.")
        return self


class StoryboardReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_video: str = Field(min_length=1)
    model: str = Field(min_length=1)
    generated_at: str = Field(min_length=1)
    language: str = Field(min_length=1)
    segments: list[StoryboardSegment] = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_segments(self) -> "StoryboardReport":
        expected_index = 1
        previous_start = -1.0
        for segment in self.segments:
            if segment.index != expected_index:
                raise ValueError("Segment indices must be continuous and start at 1.")
            if segment.start_sec < previous_start:
                raise ValueError("Segments must be sorted by start_sec.")
            expected_index += 1
            previous_start = segment.start_sec
        return self


def build_storyboard_report(
    *,
    source_video: str,
    model: str,
    draft: StoryboardDraft,
    generated_at: str | None = None,
) -> StoryboardReport:
    timestamp = generated_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    segments = [
        StoryboardSegment(
            index=segment.index,
            start_sec=segment.start_sec,
            end_sec=segment.end_sec,
            duration_sec=segment.end_sec - segment.start_sec,
            scene_summary=segment.scene_summary,
            background_summary=segment.background_summary,
            spatial_layout=segment.spatial_layout,
            lighting=segment.lighting,
            placement_space_hint=segment.placement_space_hint,
            characters=segment.characters,
            actions=segment.actions,
            camera_motion=segment.camera_motion,
            thumbnail_path=None,
        )
        for segment in draft.segments
    ]
    return StoryboardReport(
        source_video=source_video,
        model=model,
        generated_at=timestamp,
        language=draft.language,
        segments=segments,
    )
