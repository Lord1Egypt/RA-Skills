#!/usr/bin/env python3
"""
Flutter platform scanner — detects and scans Flutter projects for
colors, strings, images, and custom widgets.

Supports scan levels:
  - "resources": colors + strings + images only (fast, ~100ms)
  - "full": resources + custom widgets (default, ~300ms)
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from .base import (
    ColorEntry, CustomViewEntry, ImageEntry,
    ModuleReport, ProjectScanner, ScanReport,
    SemanticLabel, StringEntry,
)

# Directories and files to skip when scanning Dart source.
_SKIP_DIRS = frozenset((".dart_tool", ".packages", "build", ".flutter-plugins",
                        "ios", "android", "web", "macos", "linux", "windows",
                        "test", "integration_test", "coverage", "node_modules"))

# Regex patterns for Dart color extraction.
# Matches: Color(0xFF6200EE) or const Color(0xFF6200EE)
_RE_DART_COLOR_HEX = re.compile(
    r'(?:const\s+)?Color\(\s*0x([0-9A-Fa-f]{8})\s*\)',
)

# Matches: Colors.purple.shade500 or Colors.blue
_RE_DART_COLORS_CLASS = re.compile(
    r'Colors\.(\w+)(?:\.shade(\d+))?',
)

# Matches: static const Color xyz = Color(0xFF...)
_RE_COLOR_DECL = re.compile(
    r'(?:static\s+)?(?:final|const)\s+Color\s+(\w+)\s*=\s*(?:const\s+)?Color\(\s*0x([0-9A-Fa-f]{8})\s*\)',
)

# Matches: ColorScheme(primary: Color(...), ...)
_RE_THEME_COLOR_SCHEME = re.compile(
    r'ColorScheme\s*\(([^)]*(?:\([^)]*\)[^)]*)*)\)',
)

# Matches named parameters inside ColorScheme: primary: Color(0xFF...)
_RE_COLOR_SCHEME_PARAM = re.compile(
    r'(\w+)\s*:\s*(?:const\s+)?Color\(\s*0x([0-9A-Fa-f]{8})\s*\)',
)

# Matches: ThemeData(primaryColor: Color(...), ...)
_RE_THEME_DATA_COLOR = re.compile(
    r'(\w+Color|colorScheme)\s*:\s*(?:const\s+)?Color\(\s*0x([0-9A-Fa-f]{8})\s*\)',
)

# Matches Flutter widget class declarations.
_RE_DART_WIDGET_CLASS = re.compile(
    r'class\s+(\w+)\s+extends\s+(StatelessWidget|StatefulWidget|InheritedWidget|PreferredSizeWidget)',
)

# Matches a simple custom widget (not from framework packages).
_RE_CUSTOM_CLASS = re.compile(
    r'class\s+(\w+)\s+extends\s+(\w+)',
)

# .arb file key-value pattern.
_RE_ARB_KEY = re.compile(
    r'"(\w+)"\s*:\s*"((?:[^"\\]|\\.)*)"',
)

# Flutter color name → semantic role (lowered, no underscores).
# Ordered longest-first to avoid partial matches (e.g. 'onprimary' before 'primary').
_FLUTTER_COLOR_SEMANTICS: list[tuple[str, str]] = [
    ("onprimarycontainer", "on_primary_container"),
    ("onsecondarycontainer", "on_secondary_container"),
    ("onerrorcontainer", "on_error_container"),
    ("onsurfacevariant", "on_surface_variant"),
    ("primarycontainer", "primary_container"),
    ("secondarycontainer", "secondary_container"),
    ("errorcontainer", "error_container"),
    ("surfacevariant", "surface_variant"),
    ("inversesurface", "inverse_surface"),
    ("inverseprimary", "inverse_primary"),
    ("onprimary", "on_primary"),
    ("onsecondary", "on_secondary"),
    ("ontertiary", "on_tertiary"),
    ("onsurface", "on_surface"),
    ("onbackground", "on_background"),
    ("onerror", "on_error"),
    ("primary", "primary"),
    ("secondary", "secondary"),
    ("tertiary", "tertiary"),
    ("surface", "surface"),
    ("background", "background"),
    ("error", "error"),
    ("outline", "outline"),
    ("shadow", "shadow"),
    ("tint", "tint"),
]


def _discover_module(root: Path) -> Path:
    """Flutter is single-module; return lib/ directory."""
    lib_dir = root / "lib"
    return lib_dir if lib_dir.is_dir() else root


def _parse_pubspec(root: Path) -> dict:
    """
    Parse pubspec.yaml for assets, fonts, and package name.

    Returns a dict with keys: 'name', 'assets', 'fonts', 'dependencies'.
    Minimal YAML parsing (no PyYAML dep) — handles common patterns.
    """
    info: dict = {
        "name": root.name,
        "assets": [],
        "fonts": [],
        "dependencies": [],
    }

    pubspec = root / "pubspec.yaml"
    if not pubspec.is_file():
        return info

    try:
        text = pubspec.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return info

    lines = text.splitlines()
    in_assets = False
    in_fonts = False
    in_font_files = False
    in_deps = False

    for line in lines:
        stripped = line.strip()

        # Package name
        m = re.match(r'^name:\s*(\S+)', stripped)
        if m:
            info["name"] = m.group(1)

        # Section markers (simple indentation-based)
        if re.match(r'^flutter:', stripped):
            in_assets = False
            in_fonts = False
            continue
        if re.match(r'^dependencies:', stripped):
            in_deps = True
            in_assets = False
            in_fonts = False
            continue
        if re.match(r'^dev_dependencies:', stripped):
            in_deps = False
            in_assets = False
            in_fonts = False
            continue

        if in_deps and stripped.startswith('- ') and ':' in stripped:
            dep_name = stripped.lstrip('- ').split(':')[0].strip()
            info["dependencies"].append(dep_name)

        if stripped.startswith('assets:'):
            in_assets = True
            in_fonts = False
            continue
        if stripped.startswith('fonts:'):
            in_fonts = True
            in_assets = False
            in_font_files = False
            continue

        if in_assets and stripped.startswith('- '):
            path = stripped.lstrip('- ').strip()
            info["assets"].append(path)

        if in_fonts and stripped.startswith('- family:'):
            in_font_files = True
        if in_fonts and in_font_files and stripped.startswith('- '):
            path = stripped.lstrip('- ').strip()
            # Resolve relative to font family block, but keep as-is
            if path.endswith(('.ttf', '.otf')):
                info["fonts"].append(path)

    return info


def _scan_dart_colors(dart_file: Path, source_hint: str) -> list[dict]:
    """Extract color definitions from a Dart file using regex."""
    colors: list[dict] = []
    try:
        text = dart_file.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return colors

    # Static const Color declarations (highest priority)
    for m in _RE_COLOR_DECL.finditer(text):
        name = m.group(1)
        hex_val = "#" + m.group(2).upper()
        colors.append({"name": name, "value": hex_val, "source": source_hint})

    # Direct Color(0xFF...) declarations (non-const)
    seen_hex: set[str] = set()
    for m in _RE_DART_COLOR_HEX.finditer(text):
        hex_val = "#" + m.group(1).upper()
        if hex_val not in seen_hex:
            seen_hex.add(hex_val)
            # Try to find a variable name on the same line
            line_start = max(0, m.start() - 80)
            line_context = text[line_start:m.start()]
            name_match = re.search(r'(?:static\s+)?(?:final|const)\s+Color\s+(\w+)', line_context)
            name = name_match.group(1) if name_match else f"color_{hex_val[1:].lower()}"
            colors.append({"name": name, "value": hex_val, "source": source_hint})

    return colors


def _scan_dart_widgets(dart_file: Path, root: Path) -> list[dict]:
    """Extract custom widget class definitions from a Dart file."""
    views: list[dict] = []
    try:
        text = dart_file.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return views

    sf_str = str(dart_file)

    # Widget classes extending known Flutter widget types
    for m in _RE_DART_WIDGET_CLASS.finditer(text):
        cls_name, parent = m.group(1), m.group(2)
        pkg = _infer_package(dart_file, root)
        views.append({
            "name": cls_name,
            "parent": parent,
            "package": pkg,
            "file": sf_str,
        })

    return views


def _infer_package(file: Path, root: Path) -> str:
    """Infer Dart package name from file path relative to lib/."""
    try:
        # Find 'lib' in the path
        parts = file.relative_to(root).parts
        # If file is under lib/, convert to package path
        rel = file.relative_to(root / "lib") if (root / "lib") in file.parents else file.relative_to(root)
        rel_str = str(rel.with_suffix("")).replace("\\", "/").replace("/", ".")
        # Remove file name, keep directory path
        pkg_parts = rel_str.split(".")[:-1]
        return ".".join(pkg_parts) if pkg_parts else ""
    except (ValueError, AttributeError):
        return ""


def _scan_arb_strings(root: Path) -> list[dict]:
    """Scan .arb (Flutter ARB) localization files."""
    strings: list[dict] = []
    for arb_file in root.rglob("*.arb"):
        if _SKIP_DIRS & set(arb_file.parts):
            continue
        try:
            data = json.loads(arb_file.read_text(encoding="utf-8", errors="ignore"))
        except (json.JSONDecodeError, OSError):
            continue
        source_hint = str(arb_file)
        for key, value in data.items():
            # Skip metadata keys starting with @
            if key.startswith("@"):
                continue
            if isinstance(value, str) and value.strip():
                strings.append({"key": key, "value": value.strip(), "source": source_hint})
    return strings


def _scan_assets(root: Path, pubspec_info: dict) -> list[dict]:
    """Scan asset directories declared in pubspec.yaml + file system."""
    images: list[dict] = []
    seen: set[str] = set()

    # Collect image files from declared asset paths
    for asset_path in pubspec_info.get("assets", []):
        full_path = root / asset_path
        if full_path.is_dir():
            for ext in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"):
                for img_file in full_path.rglob(f"*{ext}"):
                    name = img_file.stem
                    if name not in seen:
                        seen.add(name)
                        images.append({
                            "name": name,
                            "type": ext.lstrip("."),
                            "source": str(img_file),
                        })
        elif full_path.is_file():
            name = full_path.stem
            if name not in seen:
                seen.add(name)
                ext = full_path.suffix.lstrip(".")
                images.append({
                    "name": name,
                    "type": ext or "unknown",
                    "source": str(full_path),
                })

    # Also scan common asset directories
    for img_dir in (root / "assets", root / "images"):
        if img_dir.is_dir():
            for ext in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"):
                for img_file in img_dir.rglob(f"*{ext}"):
                    name = img_file.stem
                    if name not in seen:
                        seen.add(name)
                        images.append({
                            "name": name,
                            "type": ext.lstrip("."),
                            "source": str(img_file),
                        })

    return images


class FlutterScanner(ProjectScanner):
    """Scan a Flutter project and produce a unified ScanReport."""

    def get_platform_name(self) -> str:
        return "flutter"

    def discover_modules(
        self, project_root: Path, target_module: str | None = None,
    ) -> tuple[list[tuple[str, Path]], list[str]]:
        errors: list[str] = []

        # Flutter is single-module: the root project itself
        lib_dir = _discover_module(project_root)
        if not lib_dir.is_dir():
            errors.append("No lib/ directory found in Flutter project")
            return [], errors

        # Use pubspec name if available, else directory name
        pubspec_info = _parse_pubspec(project_root)
        name = pubspec_info.get("name", project_root.name)

        return [(name, project_root)], errors

    def scan_module(
        self, name: str, mod_dir: Path, project_root: Path, level: str = "full",
    ) -> ModuleReport:
        scan_widgets = level == "full"
        pubspec_info = _parse_pubspec(mod_dir)
        lib_dir = mod_dir / "lib"
        source_hint = str(lib_dir) if lib_dir.is_dir() else str(mod_dir)

        # Scan Dart files for colors
        dart_colors: list[dict] = []
        if lib_dir.is_dir():
            for dart_file in lib_dir.rglob("*.dart"):
                if _SKIP_DIRS & set(dart_file.parts):
                    continue
                dart_colors.extend(_scan_dart_colors(dart_file, source_hint))

        # Scan strings (ARB files)
        strings = _scan_arb_strings(mod_dir)

        # Scan images from assets
        images = _scan_assets(mod_dir, pubspec_info)

        # Scan custom widgets
        views: list[dict] = []
        if scan_widgets and lib_dir.is_dir():
            for dart_file in lib_dir.rglob("*.dart"):
                if _SKIP_DIRS & set(dart_file.parts):
                    continue
                views.extend(_scan_dart_widgets(dart_file, mod_dir))

        return ModuleReport(
            name=name,
            path=str(mod_dir),
            colors=[ColorEntry(**c) for c in dart_colors],
            strings=[StringEntry(**s) for s in strings],
            images=[ImageEntry(**i) for i in images],
            custom_views=[CustomViewEntry(**v) for v in views],
        )

    def build_indices(self, report: ScanReport) -> None:
        """Build color/string/image indices for Flutter."""
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
        Annotate Flutter resources with semantic roles.

        Sources:
          1. Color name conventions matching Material 3 roles
             (primary, secondary, surface, etc.)
          2. ColorScheme parameter names in ThemeData definitions
        """
        for mod in report.modules:
            self._label_flutter_colors(mod, report)

    def _label_flutter_colors(self, mod: ModuleReport, report: ScanReport) -> None:
        """Label colors by name heuristics matching Material 3 roles."""
        for c in mod.colors:
            name_lower = c.name.lower().replace("_", "").replace("-", "")
            for keyword, role in _FLUTTER_COLOR_SEMANTICS:
                kw_lower = keyword.lower()
                if kw_lower == name_lower:
                    report.semantic_labels.append(SemanticLabel(
                        name=c.value,
                        resource_type="color",
                        semantic_role=role,
                        source="naming_convention",
                        confidence="high",
                    ))
                    break
                elif kw_lower in name_lower:
                    report.semantic_labels.append(SemanticLabel(
                        name=c.value,
                        resource_type="color",
                        semantic_role=role,
                        source="naming_convention",
                        confidence="medium",
                    ))
                    break
