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
    ModuleReport, ProjectScanner, ScanReport, StringEntry,
)
from .ios_resources import (
    scan_colorset_assets,
    scan_strings_files, scan_json_strings,
)
from .ios_assets import scan_imagesets, scan_loose_images
from .ios_swift_scan import scan_swift_single_pass


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

    def scan(
        self,
        project_root: Path,
        target_module: str | None = None,
        **kwargs,
    ) -> ScanReport:
        """
        Scan the iOS project.

        Args:
            project_root: Path to project root.
            target_module: Optional module name to focus on.
            level: "resources" (fast) or "full" (default).
        """
        level = kwargs.get("level", "full")
        report = ScanReport(platform="ios", project_root=str(project_root))
        all_modules = _discover_modules(project_root)

        if target_module:
            filtered = [(n, d) for n, d in all_modules if n == target_module]
            if not filtered:
                report.errors.append(f"Module '{target_module}' not found")
            all_modules = filtered or all_modules

        scan_views = level == "full"

        for mod_name, mod_dir in all_modules:
            mod_report = self._scan_module(
                mod_name, mod_dir, project_root, scan_views=scan_views
            )
            report.modules.append(mod_report)

        # Build indices
        report.indices["colors"] = self._build_color_index(report)
        report.indices["strings"] = self._build_string_index(report)
        report.indices["images"] = self._build_image_index(report)

        report.finalize_metadata(modules_skipped=0)
        return report

    def _scan_module(
        self, name: str, mod_dir: Path, root: Path,
        *, scan_views: bool = True,
    ) -> ModuleReport:
        # Single-pass Swift scan (colors + NSLocalizedString + optionally views)
        swift_data = scan_swift_single_pass(
            mod_dir,
            colors=True,
            strings=True,
            views=scan_views,
        )

        # Colors: xcassets colorsets + swift code colors
        raw_colors = scan_colorset_assets(mod_dir) + swift_data["colors"]

        # Strings: .strings + JSON i18n + NSLocalizedString (from swift pass)
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

    @staticmethod
    def _build_color_index(report: ScanReport) -> dict:
        idx: dict[str, str] = {}
        for mod in report.modules:
            for c in mod.colors:
                idx[c.name] = c.value
        return idx

    @staticmethod
    def _build_string_index(report: ScanReport) -> dict:
        idx: dict[str, str] = {}
        for mod in report.modules:
            for s in mod.strings:
                if s.value:
                    idx[s.key] = s.value
        return idx

    @staticmethod
    def _build_image_index(report: ScanReport) -> dict:
        idx: dict[str, str] = {}
        for mod in report.modules:
            for i in mod.images:
                idx[i.name] = i.type
        return idx
