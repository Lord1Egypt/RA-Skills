#!/usr/bin/env python3
"""Detect whether a project is a Flutter project."""

from __future__ import annotations

from pathlib import Path
from .base import PlatformDetector


class FlutterDetector(PlatformDetector):
    """Detect Flutter projects by the presence of pubspec.yaml."""

    def detect(self, project_root: Path) -> bool:
        return (project_root / "pubspec.yaml").exists()

    def platform_name(self) -> str:
        return "flutter"
