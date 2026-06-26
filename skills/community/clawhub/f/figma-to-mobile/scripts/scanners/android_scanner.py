#!/usr/bin/env python3
"""
Android platform detector and project scanner.

Wraps the existing Android module/resource/drawable/view scanners
into the unified ProjectScanner interface.

Supports scan levels:
  - "resources": colors + strings + drawables + deps (fastest)
  - "full": resources + custom views + layout analysis (default)
"""

from __future__ import annotations

from pathlib import Path

from .base import (
    ColorEntry, CustomViewEntry, DimenEntry, ImageEntry,
    ModuleReport, PlatformDetector, ProjectScanner, ScanReport,
    StringEntry, StyleEntry, TextStyleEntry,
)
from .android_modules import resolve_all_modules
from .android_resources import (
    scan_module_resources, build_color_index, build_string_index,
    build_text_style_index,
)
from .android_drawables import (
    scan_drawables, build_drawable_index,
    scan_shape_drawables, build_shape_index, DrawableShapeEntry,
)
from .android_views import scan_custom_views
from .android_deps import build_dep_graph, visible_resources
from .android_layouts import scan_layouts


class AndroidDetector(PlatformDetector):
    """Detect Android projects by the presence of settings.gradle(.kts)."""

    def detect(self, project_root: Path) -> bool:
        return (
            (project_root / "settings.gradle.kts").exists()
            or (project_root / "settings.gradle").exists()
        )

    def platform_name(self) -> str:
        return "android"


class AndroidScanner(ProjectScanner):
    """Scan an Android project and produce a unified ScanReport."""

    def scan(self, project_root: Path, target_module: str | None = None, **kwargs) -> ScanReport:
        level = kwargs.get("level", "full")
        root_str = str(project_root)
        report = ScanReport(platform="android", project_root=root_str)

        # Step 1: Discover modules
        modules = resolve_all_modules(root_str, target_module)
        report.errors.extend(modules["errors"])
        skipped = modules["skipped"]

        if not modules["scannable"]:
            report.finalize_metadata(modules_skipped=len(skipped))
            return report

        scan_views = level == "full"
        target_name = (target_module or "app").lstrip(":")

        # Step 2: Build dependency graph
        dep_graph = build_dep_graph(root_str, modules["scannable"])
        visible_mods = visible_resources(
            ":" + target_name, dep_graph
        )
        # Also try without colon prefix
        visible_mods |= visible_resources(target_name, dep_graph)

        # Step 3: Scan each module
        all_raw_resources: list[dict] = []
        for mod_name, mod_dir in modules["scannable"]:
            raw_res = scan_module_resources(mod_dir)
            all_raw_resources.append(raw_res)

            views = scan_custom_views(mod_dir) if scan_views else []

            module_report = _build_module_report(
                mod_name, mod_dir, raw_res, views
            )
            report.modules.append(module_report)

        # Step 4: Drawables for target module
        if modules["target"]:
            target_res_dir = modules["target"] / "src" / "main" / "res"
            if target_res_dir.is_dir():
                drawables = scan_drawables(target_res_dir)
                drawable_index = build_drawable_index(drawables)

                # Shape drawable scanning (structured entries)
                shape_entries = scan_shape_drawables(target_res_dir)
                shape_index = build_shape_index(shape_entries)

                for mod_report in report.modules:
                    if mod_report.name.lstrip(":") == target_name:
                        for d in drawables:
                            mod_report.images.append(ImageEntry(
                                name=d["name"],
                                type=d.get("type", "unknown"),
                                source=d.get("file", ""),
                            ))
                        # Add shape entries as type="shape" ImageEntry
                        # (deduplicate: only add shapes not already in images)
                        existing_names = {img.name for img in mod_report.images}
                        for se in shape_entries:
                            if se.name not in existing_names:
                                mod_report.images.append(ImageEntry(
                                    name=se.name,
                                    type="shape",
                                    source=se.source,
                                ))
                        break

                report.indices["images"] = drawable_index
                report.indices["drawable_shapes"] = shape_index

        # Step 5: Build lookup indices with visibility info
        report.indices["colors"] = _build_visible_color_index(
            report, visible_mods
        )
        report.indices["strings"] = _build_visible_string_index(
            report, visible_mods
        )

        # Step 5b: Build text style index
        report.indices["text_styles"] = _build_visible_text_style_index(
            report, visible_mods
        )

        # Step 6: Layout analysis (full mode only)
        if scan_views and modules["target"]:
            target_res = modules["target"] / "src" / "main" / "res"
            if target_res.is_dir():
                report.metadata["layout_analysis"] = scan_layouts(target_res)

        # Step 7: Dependency graph in metadata
        report.metadata["dependencies"] = dep_graph
        report.metadata["visible_to_target"] = sorted(visible_mods)

        report.finalize_metadata(modules_skipped=len(skipped))
        return report


def _build_visible_color_index(
    report: ScanReport, visible_mods: set[str],
) -> dict:
    """
    Build hex→@color/name index, only including colors
    from modules visible to the target.
    """
    idx: dict[str, str] = {}
    for mod in report.modules:
        # Check visibility: strip colon prefix for comparison
        mod_clean = mod.name.lstrip(":")
        mod_colon = ":" + mod_clean
        if mod_clean not in visible_mods and mod_colon not in visible_mods:
            continue
        for c in mod.colors:
            normalized = _normalize_hex(c.value)
            if normalized and normalized not in idx:
                idx[normalized] = f"@color/{c.name}"
    return idx


def _build_visible_string_index(
    report: ScanReport, visible_mods: set[str],
) -> dict:
    """Build text→@string/name index for visible modules only."""
    idx: dict[str, str] = {}
    for mod in report.modules:
        mod_clean = mod.name.lstrip(":")
        mod_colon = ":" + mod_clean
        if mod_clean not in visible_mods and mod_colon not in visible_mods:
            continue
        for s in mod.strings:
            if s.value and s.value not in idx:
                idx[s.value] = f"@string/{s.key}"
    return idx


def _build_visible_text_style_index(
    report: ScanReport, visible_mods: set[str],
) -> dict:
    """
    Build "{textSize}_{fontWeight}" → list[@style/Name] index
    for TextAppearance styles from visible modules only.
    """
    # Convert ModuleReport.text_styles back into raw dicts for build_text_style_index
    raw_modules: list[dict] = []
    for mod in report.modules:
        mod_clean = mod.name.lstrip(":")
        mod_colon = ":" + mod_clean
        if mod_clean not in visible_mods and mod_colon not in visible_mods:
            continue
        raw_modules.append({
            "text_styles": [
                {
                    "name": ts.name,
                    "text_size": ts.text_size,
                    "text_style": ts.text_style,
                    "font_family": ts.font_family,
                }
                for ts in mod.text_styles
            ]
        })
    return build_text_style_index(raw_modules)


def _normalize_hex(value: str) -> str | None:
    """Normalize color hex to uppercase 8-char #AARRGGBB."""
    value = value.strip()
    if not value.startswith("#"):
        return None
    h = value[1:].upper()
    if len(h) == 3:
        h = "FF" + "".join(c * 2 for c in h)
    elif len(h) == 4:
        h = "".join(c * 2 for c in h)
    elif len(h) == 6:
        h = "FF" + h
    elif len(h) == 8:
        pass
    else:
        return None
    return "#" + h


def _build_module_report(
    mod_name: str, mod_dir: Path,
    raw_res: dict, raw_views: list[dict],
) -> ModuleReport:
    """Convert raw scanner dicts into a typed ModuleReport."""
    res_dir = mod_dir / "src" / "main" / "res"
    source_hint = str(res_dir) if res_dir.is_dir() else str(mod_dir)

    return ModuleReport(
        name=mod_name,
        path=str(mod_dir),
        colors=[
            ColorEntry(name=c["name"], value=c["value"], source=source_hint)
            for c in raw_res.get("colors", [])
        ],
        strings=[
            StringEntry(key=s["name"], value=s["value"], source=source_hint)
            for s in raw_res.get("strings", [])
        ],
        images=[],
        custom_views=[
            CustomViewEntry(
                name=v["name"], parent=v["parent"],
                package=v.get("package", ""), file=v.get("file", ""),
            )
            for v in raw_views
        ],
        styles=[
            StyleEntry(name=s["name"], parent=s.get("parent"), items=s.get("items", {}))
            for s in raw_res.get("styles", [])
        ],
        dimens=[
            DimenEntry(name=d["name"], value=d["value"])
            for d in raw_res.get("dimens", [])
        ],
        text_styles=[
            TextStyleEntry(
                name=ts["name"],
                parent=ts.get("parent"),
                text_size=ts.get("text_size"),
                text_color=ts.get("text_color"),
                font_family=ts.get("font_family"),
                text_style=ts.get("text_style"),
                line_height=ts.get("line_height"),
                letter_spacing=ts.get("letter_spacing"),
            )
            for ts in raw_res.get("text_styles", [])
        ],
    )
