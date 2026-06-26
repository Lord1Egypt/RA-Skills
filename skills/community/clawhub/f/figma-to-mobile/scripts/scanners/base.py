#!/usr/bin/env python3
"""
Base classes and unified schema for multi-platform project scanning.

All platform scanners (Android, iOS, Flutter, etc.) produce a ScanReport
in the same format, enabling downstream tools to work platform-agnostically.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCANNER_VERSION = "2.0.0"


# ── Unified output schema (as typed dicts for documentation + runtime use) ──

@dataclass
class ColorEntry:
    name: str
    value: str
    source: str = ""


@dataclass
class StringEntry:
    key: str
    value: str
    source: str = ""


@dataclass
class ImageEntry:
    name: str
    type: str          # imageset / vector / shape / png / svg / ...
    source: str = ""


@dataclass
class CustomViewEntry:
    name: str
    parent: str
    package: str = ""
    file: str = ""


@dataclass
class StyleEntry:
    name: str
    parent: str | None = None
    items: dict[str, str] = field(default_factory=dict)


@dataclass
class DimenEntry:
    name: str
    value: str


@dataclass
class TextStyleEntry:
    """A TextAppearance / text style extracted from Android XML resources."""
    name: str
    parent: str | None = None
    text_size: str | None = None       # e.g. "16sp"
    text_color: str | None = None      # e.g. "#FF000000"
    font_family: str | None = None     # e.g. "sans-serif-medium"
    text_style: str | None = None      # bold / italic / normal
    line_height: str | None = None     # e.g. "24sp"
    letter_spacing: str | None = None  # e.g. "0.02"


@dataclass
class ModuleReport:
    name: str
    path: str
    colors: list[ColorEntry] = field(default_factory=list)
    strings: list[StringEntry] = field(default_factory=list)
    images: list[ImageEntry] = field(default_factory=list)
    custom_views: list[CustomViewEntry] = field(default_factory=list)
    styles: list[StyleEntry] = field(default_factory=list)
    dimens: list[DimenEntry] = field(default_factory=list)
    text_styles: list[TextStyleEntry] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.path,
            "colors": [{"name": c.name, "value": c.value, "source": c.source} for c in self.colors],
            "strings": [{"key": s.key, "value": s.value, "source": s.source} for s in self.strings],
            "images": [{"name": i.name, "type": i.type, "source": i.source} for i in self.images],
            "custom_views": [
                {"name": v.name, "parent": v.parent, "package": v.package, "file": v.file}
                for v in self.custom_views
            ],
            "styles": [
                {"name": s.name, "parent": s.parent, "items": s.items}
                for s in self.styles
            ],
            "dimens": [{"name": d.name, "value": d.value} for d in self.dimens],
            "text_styles": [
                {
                    "name": t.name, "parent": t.parent,
                    "text_size": t.text_size, "text_color": t.text_color,
                    "font_family": t.font_family, "text_style": t.text_style,
                    "line_height": t.line_height, "letter_spacing": t.letter_spacing,
                }
                for t in self.text_styles
            ],
        }


@dataclass
class ScanReport:
    platform: str
    project_root: str
    modules: list[ModuleReport] = field(default_factory=list)
    indices: dict[str, dict] = field(default_factory=lambda: {
        "colors": {},
        "strings": {},
        "images": {},
        "drawable_shapes": {},
        "text_styles": {},
    })
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "platform": self.platform,
            "project_root": self.project_root,
            "modules": [m.to_dict() for m in self.modules],
            "indices": self.indices,
            "errors": self.errors,
            "metadata": self.metadata,
        }

    def finalize_metadata(self, modules_skipped: int = 0) -> None:
        """Fill in metadata fields after scanning is complete."""
        self.metadata.update({
            "scan_time": datetime.now(timezone.utc).isoformat(),
            "scanner_version": SCANNER_VERSION,
            "modules_scanned": len(self.modules),
            "modules_skipped": modules_skipped,
        })


# ── Abstract base classes ──

class PlatformDetector(ABC):
    """Detect whether a project root belongs to a specific platform."""

    @abstractmethod
    def detect(self, project_root: Path) -> bool:
        """Return True if project_root looks like this platform."""
        ...

    @abstractmethod
    def platform_name(self) -> str:
        """Short identifier: 'android', 'ios', 'flutter', etc."""
        ...


class ProjectScanner(ABC):
    """Scan a project and produce a unified ScanReport."""

    @abstractmethod
    def scan(self, project_root: Path, target_module: str | None = None, **kwargs) -> ScanReport:
        """
        Scan the project and return a ScanReport.

        Args:
            project_root: Path to the project root directory.
            target_module: Optional module name to focus on.
            **kwargs: Platform-specific options (e.g., level='resources').
        """
        ...
