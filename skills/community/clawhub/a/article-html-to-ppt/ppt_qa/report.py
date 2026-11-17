from __future__ import annotations

import dataclasses
import hashlib
import json
from pathlib import Path
from typing import Any

from .models import InspectedObject, PackageInspection, SlideInspection, ValidationIssue


def _clean(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return _clean(dataclasses.asdict(value))
    if isinstance(value, dict):
        return {key: _clean(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_clean(item) for item in value]
    return value


def issue_to_dict(issue: ValidationIssue) -> dict[str, Any]:
    return _clean(issue)


def object_to_dict(obj: InspectedObject, include_raw_xml: bool = False) -> dict[str, Any]:
    data = _clean(obj)
    if not include_raw_xml:
        data.pop("raw", None)
    return data


def slide_to_dict(slide: SlideInspection, include_raw_xml: bool = False) -> dict[str, Any]:
    return {
        "slide_index": slide.slide_index,
        "slide_id": slide.slide_id,
        "objects": [object_to_dict(obj, include_raw_xml=include_raw_xml) for obj in slide.objects],
        "metrics": _clean(slide.metrics),
        "issues": [issue_to_dict(issue) for issue in slide.issues],
    }


def inspection_to_dict(inspection: PackageInspection, include_raw_xml: bool = False) -> dict[str, Any]:
    issues = list(inspection.issues)
    for slide in inspection.slides:
        issues.extend(slide.issues)
    pptx = Path(inspection.pptx_path)
    digest = hashlib.sha256(pptx.read_bytes()).hexdigest() if pptx.is_file() else None
    return {
        "schema_version": "1.0",
        "pptx": inspection.pptx_path,
        "pptx_sha256": f"sha256:{digest}" if digest else None,
        "slide_count": inspection.slide_count,
        "status": inspection.status,
        "metrics": _clean(inspection.metrics),
        "slides": [slide_to_dict(slide, include_raw_xml=include_raw_xml) for slide in inspection.slides],
        "issues": [issue_to_dict(issue) for issue in issues],
    }


def write_inspection(
    inspection: PackageInspection,
    output: Path,
    *,
    include_raw_xml: bool = False,
) -> dict[str, Any]:
    data = inspection_to_dict(inspection, include_raw_xml=include_raw_xml)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return data
