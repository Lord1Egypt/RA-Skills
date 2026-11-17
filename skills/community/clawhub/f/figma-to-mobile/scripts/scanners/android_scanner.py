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

import re
import xml.etree.ElementTree as ET
from pathlib import Path

from .base import (
    ColorEntry, CustomViewEntry, DimenEntry, ImageEntry,
    ModuleReport, PlatformDetector, ProjectScanner, ScanReport,
    SemanticLabel, StringEntry, StyleEntry, TextStyleEntry,
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

# Theme attrib names that map to Material Design semantic roles.
_THEME_COLOR_ROLES: dict[str, str] = {
    "colorPrimary": "primary",
    "colorPrimaryDark": "primary_dark",
    "colorPrimaryVariant": "primary_variant",
    "colorOnPrimary": "on_primary",
    "colorSecondary": "secondary",
    "colorSecondaryVariant": "secondary_variant",
    "colorOnSecondary": "on_secondary",
    "colorSurface": "surface",
    "colorOnSurface": "on_surface",
    "colorBackground": "background",
    "colorOnBackground": "on_background",
    "colorError": "error",
    "colorOnError": "on_error",
    "android:colorForeground": "foreground",
    "android:colorBackground": "background",
}

# Dimen name → size category mapping for common spacing tokens.
_DIMEN_SPACING_MAP: list[tuple[str, str]] = [
    ("spacing_xxs", "spacing_xxs"),
    ("spacing_xs", "spacing_xs"),
    ("spacing_sm", "spacing_sm"),
    ("spacing_md", "spacing_md"),
    ("spacing_lg", "spacing_lg"),
    ("spacing_xl", "spacing_xl"),
    ("spacing_xxl", "spacing_xxl"),
]

# Color name keyword → semantic role (lower confidence).
# Ordered longest-first to avoid partial matches.
_COLOR_NAME_SEMANTICS: list[tuple[str, str]] = [
    ("onprimary", "on_primary"),
    ("onsecondary", "on_secondary"),
    ("onsurface", "on_surface"),
    ("onbackground", "on_background"),
    ("onerror", "on_error"),
    ("primary", "primary"),
    ("secondary", "secondary"),
    ("surface", "surface"),
    ("background", "background"),
    ("error", "error"),
    ("accent", "accent"),
]

# Text style name keyword → semantic role.
_TEXT_STYLE_SEMANTICS: list[tuple[str, str]] = [
    ("headline", "headline"),
    ("subtitle", "subtitle"),
    ("body1", "body"),
    ("body2", "body_small"),
    ("body", "body"),
    ("title", "title"),
    ("caption", "caption"),
    ("label", "label"),
    ("button", "button"),
    ("overline", "overline"),
]


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

    def get_platform_name(self) -> str:
        return "android"

    def discover_modules(
        self, project_root: Path, target_module: str | None = None,
    ) -> tuple[list[tuple[str, Path]], list[str]]:
        root_str = str(project_root)
        modules_data = resolve_all_modules(root_str, target_module)

        modules: list[tuple[str, Path]] = []
        errors: list[str] = modules_data["errors"]

        self._target_dir = modules_data.get("target")
        self._skipped = modules_data["skipped"]
        self._all_raw_resources: list[dict] = []

        for mod_name, mod_dir in modules_data["scannable"]:
            modules.append((mod_name, Path(mod_dir) if isinstance(mod_dir, str) else mod_dir))

        if not modules:
            errors.append("No scannable modules found in project")

        return modules, errors

    def scan_module(
        self, name: str, mod_dir: Path, project_root: Path, level: str = "full",
    ) -> ModuleReport:
        scan_views = level == "full"
        mod_dir_str = str(mod_dir)
        mod_root = Path(mod_dir_str)

        raw_res = scan_module_resources(mod_root)
        self._all_raw_resources.append(raw_res)

        views = scan_custom_views(mod_root) if scan_views else []

        res_dir = mod_root / "src" / "main" / "res"
        source_hint = str(res_dir) if res_dir.is_dir() else mod_dir_str

        return ModuleReport(
            name=name,
            path=mod_dir_str,
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
                for v in views
            ],
            styles=[
                StyleEntry(name=s["name"], parent=s.get("parent"),
                           items=s.get("items", {}))
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

    def after_modules_scanned(self, report: ScanReport, project_root: Path,
                              target_module: str | None = None) -> None:
        """Android extra processing: drawables, dependency analysis, layout."""
        root_str = str(project_root)
        target_dir = getattr(self, "_target_dir", None)
        skipped = getattr(self, "_skipped", [])
        all_raw = getattr(self, "_all_raw_resources", [])

        # Build dependency graph from discovered modules
        scannable = [
            (m.name, Path(m.path)) for m in report.modules
        ]
        dep_graph = {}
        visible_mods: set[str] = set()
        if scannable:
            dep_graph = build_dep_graph(root_str, scannable)
            target_name = (target_module or "app").lstrip(":")
            visible_mods = visible_resources(":" + target_name, dep_graph)
            visible_mods |= visible_resources(target_name, dep_graph)

        # Drawables for target module
        if target_dir:
            target_path = Path(target_dir) if isinstance(target_dir, str) else target_dir
            target_res = target_path / "src" / "main" / "res"
            if target_res.is_dir():
                drawables = scan_drawables(target_res)
                drawable_index = build_drawable_index(drawables)
                shape_entries = scan_shape_drawables(target_res)
                shape_index = build_shape_index(shape_entries)

                target_name = (target_module or "app").lstrip(":")
                for mod_report in report.modules:
                    mod_clean = mod_report.name.lstrip(":")
                    if mod_clean == target_name:
                        for d in drawables:
                            mod_report.images.append(ImageEntry(
                                name=d["name"],
                                type=d.get("type", "unknown"),
                                source=d.get("file", ""),
                            ))
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

        # Build dependency-aware color / string / text_style indices
        report.indices["colors"] = self._build_visible_color_index(
            report, visible_mods,
        )
        report.indices["strings"] = self._build_visible_string_index(
            report, visible_mods,
        )
        report.indices["text_styles"] = self._build_visible_text_style_index(
            report, visible_mods,
        )

        # Layout analysis (full mode only)
        if target_dir:
            target_path = Path(target_dir) if isinstance(target_dir, str) else target_dir
            target_res = target_path / "src" / "main" / "res"
            if target_res.is_dir():
                report.metadata["layout_analysis"] = scan_layouts(target_res)

        report.metadata["dependencies"] = dep_graph
        report.metadata["visible_to_target"] = sorted(visible_mods)

    def build_indices(self, report: ScanReport) -> None:
        """Indices built in after_modules_scanned; no-op here."""
        pass

    def build_semantic_labels(self, report: ScanReport) -> None:
        """
        Annotate resources with semantic roles from themes.xml and naming conventions.

        Sources (highest confidence first):
          1. Direct theme mapping: <item name="colorPrimary">@color/xyz</item>
          2. Material Design naming: colorPrimary, colorSurface, colorOnPrimary
          3. Resource name heuristics: "primary", "surface", "background", etc.
          4. Dimen naming: "spacing_*" patterns
          5. Text style naming: "Body", "Title", "Headline", etc.
        """
        # Map theme color references to actual hex values
        color_ref_to_hex = self._build_color_ref_map(report)

        # Source 1 & 2: Parse themes.xml for explicit theme role mappings
        for mod in report.modules:
            mod_path = Path(mod.path)
            values_dir = mod_path / "src" / "main" / "res" / "values"
            if not values_dir.is_dir():
                continue

            for pattern in ("themes*.xml", "styles*.xml"):
                for xml_file in sorted(values_dir.glob(pattern)):
                    self._parse_theme_colors(
                        xml_file, color_ref_to_hex, report,
                    )

        # Source 3: Color naming conventions
        for mod in report.modules:
            for c in mod.colors:
                label = self._label_by_name(c.name, _COLOR_NAME_SEMANTICS,
                                            "color")
                if label:
                    report.semantic_labels.append(label)

        # Source 4: Dimen spacing semantics
        for mod in report.modules:
            for d in mod.dimens:
                label = self._label_by_name(
                    d.name, _DIMEN_SPACING_MAP, "dimen",
                )
                if label:
                    report.semantic_labels.append(SemanticLabel(
                        name=d.value,
                        resource_type="dimen",
                        semantic_role=label.semantic_role,
                        source="naming_convention",
                        confidence="medium",
                    ))

        # Source 5: Text style semantics
        for mod in report.modules:
            for ts in mod.text_styles:
                label = self._label_by_name(
                    ts.name, _TEXT_STYLE_SEMANTICS, "text_style",
                )
                if label:
                    report.semantic_labels.append(SemanticLabel(
                        name=f"@style/{ts.name}",
                        resource_type="text_style",
                        semantic_role=label.semantic_role,
                        source="naming_convention",
                        confidence="medium",
                    ))

    # ── Private helpers ──

    def _build_color_ref_map(self, report: ScanReport) -> dict[str, str]:
        """Build @color/name → normalized hex map from all modules."""
        ref_map: dict[str, str] = {}
        for mod in report.modules:
            for c in mod.colors:
                ref_map[f"@color/{c.name}"] = c.value
                # Also store without @color/ prefix
                ref_map[c.name] = c.value
        return ref_map

    def _parse_theme_colors(
        self, xml_file: Path, ref_map: dict[str, str], report: ScanReport,
    ) -> None:
        """
        Parse themes.xml / styles.xml for semantic color assignments.

        Looks for pattern:
          <item name="colorPrimary">@color/purple_500</item>
          <item name="colorOnPrimary">@color/white</item>
        """
        try:
            tree = ET.parse(xml_file)
        except ET.ParseError:
            return

        ANDROID_NS = "http://schemas.android.com/apk/res/android"

        for elem in tree.iter():
            if elem.tag == "style":
                # Direct children with <item name="colorPrimary"> patterns
                for item in elem.findall("item"):
                    item_name = item.get("name", "")
                    if item_name in _THEME_COLOR_ROLES:
                        resource_ref = (item.text or "").strip()
                        hex_val = ref_map.get(resource_ref, resource_ref)
                        role = _THEME_COLOR_ROLES[item_name]
                        report.semantic_labels.append(SemanticLabel(
                            name=hex_val,
                            resource_type="color",
                            semantic_role=role,
                            source="theme_mapping",
                            confidence="high",
                        ))

                # Also check android:xxx attributes on the style itself
                for attr_key, attr_val in elem.attrib.items():
                    if attr_key in _THEME_COLOR_ROLES or \
                       attr_key.replace(f"{{{ANDROID_NS}}}", "android:") in _THEME_COLOR_ROLES:
                        role_key = attr_key.replace(f"{{{ANDROID_NS}}}", "android:")
                        if role_key in _THEME_COLOR_ROLES:
                            role = _THEME_COLOR_ROLES[role_key]
                            hex_val = ref_map.get(attr_val, attr_val)
                            report.semantic_labels.append(SemanticLabel(
                                name=hex_val,
                                resource_type="color",
                                semantic_role=role,
                                source="theme_mapping",
                                confidence="high",
                            ))

    def _label_by_name(
        self, name: str, mapping: list[tuple[str, str]], resource_type: str,
    ) -> SemanticLabel | None:
        """Check if a resource name matches known semantic keywords."""
        name_lower = name.lower().replace("_", "").replace("-", "")
        for keyword, role in mapping:
            kw_lower = keyword.lower().replace("_", "").replace("-", "")
            if kw_lower in name_lower:
                return SemanticLabel(
                    name=name,
                    resource_type=resource_type,
                    semantic_role=role,
                    source="naming_convention",
                    confidence="medium",
                )
        return None

    def _build_visible_color_index(
        self, report: ScanReport, visible_mods: set[str],
    ) -> dict:
        """Build hex→@color/name index, only including visible modules."""
        idx: dict[str, str] = {}
        for mod in report.modules:
            mod_clean = mod.name.lstrip(":")
            mod_colon = ":" + mod_clean
            if mod_clean not in visible_mods and mod_colon not in visible_mods:
                continue
            for c in mod.colors:
                normalized = self._normalize_hex(c.value)
                if normalized and normalized not in idx:
                    idx[normalized] = f"@color/{c.name}"
        return idx

    def _build_visible_string_index(
        self, report: ScanReport, visible_mods: set[str],
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
        self, report: ScanReport, visible_mods: set[str],
    ) -> dict:
        """Build {textSize}_{fontWeight} → list[@style/Name] index."""
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

    @staticmethod
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
