#!/usr/bin/env python3
"""
iOS platform scanner — integrates detector, resources, assets, and views
into the unified ProjectScanner interface.

Supports scan levels:
  - "resources": colors + strings + images only (fastest, ~100ms)
  - "full": resources + custom views (default, ~300ms)
"""

from __future__ import annotations

import re
from pathlib import Path

from .base import (
    ColorEntry, CustomViewEntry, ImageEntry,
    ModuleReport, ProjectScanner, ScanReport,
    SemanticLabel, StringEntry,
)
from .ios_resources import (
    scan_colorset_assets,
    scan_strings_files, scan_json_strings,
)
from .ios_assets import scan_imagesets, scan_loose_images
from .ios_swift_scan import scan_swift_single_pass

# iOS color set name → semantic role mappings.
# Ordered longest-first to avoid partial matches.
_COLORSET_SEMANTICS: list[tuple[str, str]] = [
    ("secondarylabel", "text_secondary"),
    ("placeholdertext", "text_placeholder"),
    ("systemgroupedbackground", "surface"),
    ("systembackground", "background"),
    ("accentcolor", "primary"),
    ("primarycolor", "primary"),
    ("secondarycolor", "secondary"),
    ("tertiarycolor", "tertiary"),
    ("surfacecolor", "surface"),
    ("backgroundcolor", "background"),
    ("errorcolor", "error"),
    ("tintcolor", "tint"),
    ("labelcolor", "text_primary"),
    ("accent", "primary"),
    ("primary", "primary"),
    ("secondary", "secondary"),
    ("tertiary", "tertiary"),
    ("surface", "surface"),
    ("background", "background"),
    ("error", "error"),
    ("tint", "tint"),
    ("label", "text_primary"),
    ("separator", "separator"),
]


def _discover_modules(project_root: Path) -> list[tuple[str, Path]]:
    """
    Discover iOS modules/targets from project structure.

    Strategy:
    1. Podfile targets → directory names
    2. .xcodeproj name → same-name sibling directory
    3. Fallback → any directory containing Swift files
    """
    modules: list[tuple[str, Path]] = []
    seen: set[str] = set()

    # From Podfile targets
    podfile = project_root / "Podfile"
    if podfile.is_file():
        try:
            text = podfile.read_text(encoding="utf-8", errors="ignore")
            for m in re.finditer(r"^target\s+'(\w+)'", text, re.MULTILINE):
                name = m.group(1)
                mod_dir = project_root / name
                if mod_dir.is_dir() and name not in seen:
                    seen.add(name)
                    modules.append((name, mod_dir))
        except OSError:
            pass

    # From .xcodeproj name
    if not modules:
        for item in project_root.iterdir():
            if item.suffix == ".xcodeproj":
                name = item.stem
                mod_dir = project_root / name
                if mod_dir.is_dir() and name not in seen:
                    seen.add(name)
                    modules.append((name, mod_dir))

    # Fallback: project root itself as single module
    if not modules:
        modules.append((project_root.name, project_root))

    return modules


class IOSScanner(ProjectScanner):
    """Scan an iOS project and produce a unified ScanReport."""

    def get_platform_name(self) -> str:
        return "ios"

    def discover_modules(
        self, project_root: Path, target_module: str | None = None,
    ) -> tuple[list[tuple[str, Path]], list[str]]:
        all_modules = _discover_modules(project_root)
        errors: list[str] = []

        if target_module:
            filtered = [(n, d) for n, d in all_modules if n == target_module]
            if not filtered:
                errors.append(f"Module '{target_module}' not found in iOS project")
            modules = filtered or all_modules
        else:
            modules = all_modules

        if not modules:
            errors.append("No iOS modules found in project")

        return modules, errors

    def scan_module(
        self, name: str, mod_dir: Path, project_root: Path, level: str = "full",
    ) -> ModuleReport:
        scan_views = level == "full"

        # Single-pass Swift scan (colors + strings + optionally views)
        swift_data = scan_swift_single_pass(
            mod_dir,
            colors=True,
            strings=True,
            views=scan_views,
        )

        # Colors: xcassets colorsets + swift code colors
        raw_colors = scan_colorset_assets(mod_dir) + swift_data["colors"]

        # Strings: .strings + JSON i18n + NSLocalizedString
        raw_strings = (
            scan_strings_files(mod_dir)
            + scan_json_strings(mod_dir)
            + swift_data["strings"]
        )

        # Images: xcassets imagesets + loose
        raw_images = scan_imagesets(mod_dir) + scan_loose_images(mod_dir)

        # Views: from swift single-pass
        raw_views = swift_data["views"] if scan_views else []

        return ModuleReport(
            name=name,
            path=str(mod_dir),
            colors=[ColorEntry(**c) for c in raw_colors],
            strings=[StringEntry(**s) for s in raw_strings],
            images=[ImageEntry(**i) for i in raw_images],
            custom_views=[CustomViewEntry(**v) for v in raw_views],
        )

    def build_indices(self, report: ScanReport) -> None:
        """Build color/string/image indices for iOS."""
        idx_colors: dict[str, str] = {}
        for mod in report.modules:
            for c in mod.colors:
                if c.name not in idx_colors:
                    idx_colors[c.name] = c.value
        report.indices["colors"] = idx_colors

        idx_strings: dict[str, str] = {}
        for mod in report.modules:
            for s in mod.strings:
                if s.value:
                    idx_strings[s.key] = s.value
        report.indices["strings"] = idx_strings

        idx_images: dict[str, str] = {}
        for mod in report.modules:
            for i in mod.images:
                if i.name not in idx_images:
                    idx_images[i.name] = i.type
        report.indices["images"] = idx_images

    def build_semantic_labels(self, report: ScanReport) -> None:
        """
        Annotate iOS resources with semantic roles.

        Sources:
          1. Asset Catalog color set names → semantic roles
             (e.g. "AccentColor" → primary, "BackgroundColor" → background)
          2. Swift code color variable names → heuristics
             (e.g. "let primaryColor = UIColor(...)")
        """
        for mod in report.modules:
            self._label_ios_colors(mod, report)

    def _label_ios_colors(self, mod: ModuleReport, report: ScanReport) -> None:
        """Label iOS colors from Asset Catalog naming and code conventions."""
        for c in mod.colors:
            # Source 1: Asset Catalog naming (highest confidence)
            name_clean = c.name.lower().replace(" ", "").replace("_", "").replace("-", "")
            for keyword, role in _COLORSET_SEMANTICS:
                kw_clean = keyword.lower().replace(" ", "").replace("_", "").replace("-", "")
                if kw_clean == name_clean:
                    report.semantic_labels.append(SemanticLabel(
                        name=c.value if c.value else c.name,
                        resource_type="color",
                        semantic_role=role,
                        source="asset_naming",
                        confidence="high",
                    ))
                    break
                elif kw_clean in name_clean:
                    report.semantic_labels.append(SemanticLabel(
                        name=c.value if c.value else c.name,
                        resource_type="color",
                        semantic_role=role,
                        source="asset_naming",
                        confidence="medium",
                    ))
                    break
