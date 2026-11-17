from __future__ import annotations

import posixpath
import re
import zipfile
from pathlib import Path
from typing import Any, Optional
from urllib.parse import unquote, urlparse

from lxml import etree

from .models import IssueFactory, PackageInspection

REL_NS = {"pr": "http://schemas.openxmlformats.org/package/2006/relationships"}
P_NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main"}


def _load_json_count(data: Optional[dict[str, Any]], keys: list[str]) -> Optional[int]:
    if not isinstance(data, dict):
        return None
    cursor: Any = data
    for key in keys:
        if not isinstance(cursor, dict) or key not in cursor:
            return None
        cursor = cursor[key]
    return cursor if isinstance(cursor, int) else None


def _part_for_rels(rels_name: str) -> str:
    if rels_name == "_rels/.rels":
        return ""
    directory, filename = posixpath.split(rels_name)
    source_dir = directory.rsplit("/_rels", 1)[0]
    source_name = filename[:-5]
    return posixpath.normpath(posixpath.join(source_dir, source_name))


def _resolve_target(rels_name: str, target: str) -> str:
    source_part = _part_for_rels(rels_name)
    base_dir = posixpath.dirname(source_part)
    resolved = posixpath.normpath(posixpath.join(base_dir, unquote(target)))
    return resolved.lstrip("/")


def _is_external_path(target: str) -> bool:
    parsed = urlparse(target)
    if parsed.scheme in {"http", "https", "mailto"}:
        return False
    if parsed.scheme == "file":
        return True
    if re.match(r"^[A-Za-z]:[\\/]", target):
        return True
    return target.startswith("/") or target.startswith("\\\\")


def _is_local_file_reference(target: str) -> bool:
    parsed = urlparse(target)
    return parsed.scheme == "file" or re.match(r"^[A-Za-z]:[\\/]", target) is not None


def inspect_package(
    pptx_path: Path,
    *,
    ppt_ir: Optional[dict[str, Any]] = None,
    build_manifest: Optional[dict[str, Any]] = None,
) -> PackageInspection:
    factory = IssueFactory("pptx-package-inspector")
    inspection = PackageInspection(pptx_path=str(pptx_path))

    try:
        with zipfile.ZipFile(pptx_path) as package:
            corrupt_member = package.testzip()
            if corrupt_member is not None:
                inspection.issues.append(
                    factory.create(
                        "PPTX_PACKAGE_CORRUPT",
                        "fatal",
                        "package",
                        "PPTX zip integrity check failed.",
                        evidence={"member": corrupt_member},
                    )
                )
                inspection.status = "failed"
                return inspection
            names = set(package.namelist())
            _check_required_parts(names, inspection, factory)
            slide_names = sorted(name for name in names if re.match(r"ppt/slides/slide\d+\.xml$", name))
            inspection.slide_count = len(slide_names)
            _check_slide_rels(names, slide_names, inspection, factory)
            _check_relationships(package, names, inspection, factory)
            _check_slide_count(inspection, factory, ppt_ir=ppt_ir, build_manifest=build_manifest)
    except (OSError, zipfile.BadZipFile) as exc:
        inspection.issues.append(
            factory.create(
                "PPTX_PACKAGE_CORRUPT",
                "fatal",
                "package",
                "PPTX is not a readable zip package.",
                evidence={"error": str(exc)},
            )
        )
        inspection.status = "failed"
        return inspection

    inspection.status = "failed" if any(issue.severity in {"error", "fatal"} for issue in inspection.issues) else "passed"
    return inspection


def _check_required_parts(names: set[str], inspection: PackageInspection, factory: IssueFactory) -> None:
    required = {
        "[Content_Types].xml": "PPTX_CONTENT_TYPE_MISSING",
        "_rels/.rels": "PPTX_BROKEN_RELATIONSHIP",
        "ppt/presentation.xml": "PPTX_PRESENTATION_XML_MISSING",
        "ppt/_rels/presentation.xml.rels": "PPTX_BROKEN_RELATIONSHIP",
    }
    for part, code in required.items():
        if part not in names:
            inspection.issues.append(factory.create(code, "fatal", "package", f"Required package part is missing: {part}", evidence={"part": part}))
    for prefix, code in [
        ("ppt/theme/", "PPTX_CONTENT_TYPE_MISSING"),
        ("ppt/slideMasters/", "PPTX_CONTENT_TYPE_MISSING"),
        ("ppt/slideLayouts/", "PPTX_CONTENT_TYPE_MISSING"),
    ]:
        if not any(name.startswith(prefix) for name in names):
            inspection.issues.append(factory.create(code, "error", "package", f"Required package folder is missing or empty: {prefix}", evidence={"prefix": prefix}))


def _check_slide_rels(names: set[str], slide_names: list[str], inspection: PackageInspection, factory: IssueFactory) -> None:
    if not slide_names:
        inspection.issues.append(factory.create("PPTX_PRESENTATION_XML_MISSING", "fatal", "package", "No slide XML parts were found.", evidence={}))
    for slide_name in slide_names:
        rels_name = slide_name.replace("ppt/slides/", "ppt/slides/_rels/") + ".rels"
        if rels_name not in names:
            slide_id = Path(slide_name).stem
            inspection.issues.append(
                factory.create(
                    "PPTX_SLIDE_RELATIONSHIP_MISSING",
                    "fatal",
                    "package",
                    f"Slide relationship part is missing: {rels_name}",
                    slide_id=slide_id,
                    evidence={"slide_part": slide_name, "rels_part": rels_name},
                )
            )


def _check_relationships(
    package: zipfile.ZipFile,
    names: set[str],
    inspection: PackageInspection,
    factory: IssueFactory,
) -> None:
    rels_names = [name for name in names if name.endswith(".rels")]
    for rels_name in sorted(rels_names):
        try:
            root = etree.fromstring(package.read(rels_name))
        except etree.XMLSyntaxError as exc:
            inspection.issues.append(factory.create("PPTX_BROKEN_RELATIONSHIP", "fatal", "package", "Relationship XML is not parseable.", evidence={"rels": rels_name, "error": str(exc)}))
            continue
        for rel in root.xpath("//pr:Relationship", namespaces=REL_NS):
            target = rel.get("Target") or ""
            rel_type = rel.get("Type") or ""
            mode = rel.get("TargetMode")
            if not target:
                continue
            if mode == "External":
                if _is_external_path(target):
                    inspection.issues.append(factory.create("PPTX_EXTERNAL_ABSOLUTE_PATH", "error", "package", "External relationship uses a local or absolute path.", evidence={"rels": rels_name, "target": target}))
                if _is_local_file_reference(target):
                    inspection.issues.append(factory.create("PPTX_LOCAL_FILE_REFERENCE", "error", "package", "External relationship points to a local file.", evidence={"rels": rels_name, "target": target}))
                continue
            if _is_external_path(target):
                inspection.issues.append(factory.create("PPTX_EXTERNAL_ABSOLUTE_PATH", "error", "package", "Relationship target is an absolute local path.", evidence={"rels": rels_name, "target": target}))
                continue
            resolved = _resolve_target(rels_name, target)
            if resolved not in names:
                code = "PPTX_BROKEN_RELATIONSHIP"
                if "/media/" in resolved or "image" in rel_type:
                    code = "PPTX_MISSING_MEDIA"
                elif "/embeddings/" in resolved or "package" in rel_type:
                    code = "PPTX_MISSING_CHART_DATA"
                inspection.issues.append(
                    factory.create(
                        code,
                        "fatal" if code in {"PPTX_MISSING_MEDIA", "PPTX_MISSING_CHART_DATA"} else "error",
                        "package",
                        f"Relationship target does not exist: {target}",
                        evidence={"rels": rels_name, "target": target, "resolved": resolved, "type": rel_type},
                    )
                )


def _check_slide_count(
    inspection: PackageInspection,
    factory: IssueFactory,
    *,
    ppt_ir: Optional[dict[str, Any]],
    build_manifest: Optional[dict[str, Any]],
) -> None:
    expected = _load_json_count(ppt_ir, ["deck", "logical_slide_count"])
    physical = _load_json_count(ppt_ir, ["deck", "physical_slide_count"])
    build_count = _load_json_count(build_manifest, ["slide_count"])
    for label, count in [("ppt_ir.logical_slide_count", expected), ("ppt_ir.physical_slide_count", physical), ("build_manifest.slide_count", build_count)]:
        if count is None:
            continue
        expected_count = count
        if expected_count != inspection.slide_count:
            inspection.issues.append(
                factory.create(
                    "PPTX_SLIDE_COUNT_MISMATCH",
                    "error",
                    "package",
                    f"Slide count mismatch against {label}.",
                    evidence={"actual_slide_count": inspection.slide_count, "expected_slide_count": expected_count, "source": label},
                )
            )
