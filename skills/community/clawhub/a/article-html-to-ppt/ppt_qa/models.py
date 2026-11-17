from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


Severity = str


@dataclass
class Thresholds:
    objects_per_slide_warn: int = 180
    objects_per_slide_error: int = 300
    text_boxes_per_100_characters_warn: float = 15.0
    text_boxes_per_100_characters_error: float = 25.0
    tiny_object_warn: int = 60
    tiny_object_error: int = 120
    tiny_width_or_height_in: float = 0.05
    tiny_area_sq_in: float = 0.003
    whole_slide_raster_area_ratio: float = 0.90
    low_resolution_ppi: int = 110
    large_image_area_ratio: float = 0.30


@dataclass
class ValidationIssue:
    issue_id: str
    issue_code: str
    severity: Severity
    category: str
    detector: str
    slide_id: Optional[str]
    object_id: Optional[str]
    ppt_shape_id: Optional[int]
    evidence: dict[str, Any]
    message: str
    repair_action: Optional[dict[str, Any]] = None
    repair_status: str = "pending"
    verification: Optional[dict[str, Any]] = None


@dataclass
class InspectedObject:
    object_id: str
    slide_id: str
    shape_id: int
    shape_type: str
    name: str
    x_in: float
    y_in: float
    w_in: float
    h_in: float
    area_ratio: float
    text: str
    font_sizes_pt: list[Optional[float]] = field(default_factory=list)
    font_colors: list[str] = field(default_factory=list)
    fill_colors: list[str] = field(default_factory=list)
    line_colors: list[str] = field(default_factory=list)
    source_relationship: Optional[str] = None
    font_families: list[str] = field(default_factory=list)
    image_ext: Optional[str] = None
    image_px: Optional[dict[str, int]] = None
    geometry_type: Optional[str] = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class SlideInspection:
    slide_index: int
    slide_id: str
    objects: list[InspectedObject] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    issues: list[ValidationIssue] = field(default_factory=list)


@dataclass
class PackageInspection:
    pptx_path: str
    slide_count: int = 0
    metrics: dict[str, Any] = field(default_factory=dict)
    issues: list[ValidationIssue] = field(default_factory=list)
    slides: list[SlideInspection] = field(default_factory=list)
    status: str = "passed"


class IssueFactory:
    def __init__(self, detector: str) -> None:
        self.detector = detector
        self._counter = 0

    def create(
        self,
        issue_code: str,
        severity: Severity,
        category: str,
        message: str,
        *,
        slide_id: Optional[str] = None,
        object_id: Optional[str] = None,
        ppt_shape_id: Optional[int] = None,
        evidence: Optional[dict[str, Any]] = None,
        repair_action: Optional[dict[str, Any]] = None,
        repair_status: str = "pending",
    ) -> ValidationIssue:
        self._counter += 1
        return ValidationIssue(
            issue_id=f"QA-{self._counter:04d}",
            issue_code=issue_code,
            severity=severity,
            category=category,
            detector=self.detector,
            slide_id=slide_id,
            object_id=object_id,
            ppt_shape_id=ppt_shape_id,
            evidence=evidence or {},
            message=message,
            repair_action=repair_action,
            repair_status=repair_status,
        )
