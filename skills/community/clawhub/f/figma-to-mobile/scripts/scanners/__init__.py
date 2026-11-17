# figma-to-mobile project scanners
#
# Platform-agnostic base classes:
from .base import (
    PlatformDetector,
    ProjectScanner,
    ScanReport,
    ModuleReport,
    ColorEntry,
    StringEntry,
    ImageEntry,
    CustomViewEntry,
    StyleEntry,
    DimenEntry,
    TextStyleEntry,
    SemanticLabel,
    SCANNER_VERSION,
)

# Android scanner:
from .android_scanner import AndroidDetector, AndroidScanner
from .android_drawables import DrawableShapeEntry

# iOS scanner:
from .ios_scanner import IOSScanner
from .ios_detector import IOSDetector

# Flutter scanner:
from .flutter_scanner import FlutterScanner
from .flutter_detector import FlutterDetector

# Registry of all known platform detectors and their scanners
PLATFORM_REGISTRY: list[tuple[PlatformDetector, type[ProjectScanner]]] = [
    (AndroidDetector(), AndroidScanner),
    (IOSDetector(), IOSScanner),
    (FlutterDetector(), FlutterScanner),
]

__all__ = [
    # Base
    "PlatformDetector",
    "ProjectScanner",
    "ScanReport",
    "ModuleReport",
    "ColorEntry",
    "StringEntry",
    "ImageEntry",
    "CustomViewEntry",
    "StyleEntry",
    "DimenEntry",
    "TextStyleEntry",
    "SemanticLabel",
    "SCANNER_VERSION",
    # Android
    "AndroidDetector",
    "AndroidScanner",
    "DrawableShapeEntry",
    # iOS
    "IOSDetector",
    "IOSScanner",
    # Flutter
    "FlutterDetector",
    "FlutterScanner",
    # Registry
    "PLATFORM_REGISTRY",
]
