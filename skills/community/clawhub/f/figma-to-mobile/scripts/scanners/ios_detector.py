#!/usr/bin/env python3
"""Detect whether a project is an iOS/macOS Xcode project."""

from __future__ import annotations
from pathlib import Path
from .base import PlatformDetector


class IOSDetector(PlatformDetector):
    """Detect iOS projects by .xcodeproj, .xcworkspace, or Package.swift."""

    def detect(self, project_root: Path) -> bool:
        # .xcodeproj or .xcworkspace directory
        for item in project_root.iterdir():
            if item.is_dir() and (
                item.suffix == ".xcodeproj"
                or item.suffix == ".xcworkspace"
            ):
                return True
        # SPM project
        if (project_root / "Package.swift").exists():
            return True
        return False

    def platform_name(self) -> str:
        return "ios"
