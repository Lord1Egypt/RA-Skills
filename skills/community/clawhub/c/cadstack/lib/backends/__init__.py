"""CAD Backend implementations.

This package provides abstracted backends for various CAD platforms.
All backends inherit from CADBackend and implement a common interface.
"""

from .base import CADBackend, CADObject, CADDocument, Material

# Attempt to import available backends
_available_backends = {}

# CadQuery (pure Python, pip install)
try:
    from .cadquery import CadQueryBackend, CADQUERY_AVAILABLE
    if CADQUERY_AVAILABLE:
        _available_backends["cadquery"] = CadQueryBackend
except ImportError:
    CADQUERY_AVAILABLE = False

# FreeCAD (requires FreeCAD installation)
try:
    from .freecad import FreeCADBackend, FREECAD_AVAILABLE
    if FREECAD_AVAILABLE:
        _available_backends["freecad"] = FreeCADBackend
except ImportError:
    FREECAD_AVAILABLE = False

# AutoCAD (Windows only)
try:
    from .autocad import AutoCADBackend, WIN32_AVAILABLE as AUTOCAD_AVAILABLE
    if AUTOCAD_AVAILABLE:
        _available_backends["autocad"] = AutoCADBackend
except ImportError:
    AUTOCAD_AVAILABLE = False

# SolidWorks (Windows only)
try:
    from .solidworks import SolidWorksBackend, WIN32_AVAILABLE as SOLIDWORKS_AVAILABLE
    if SOLIDWORKS_AVAILABLE:
        _available_backends["solidworks"] = SolidWorksBackend
except ImportError:
    SOLIDWORKS_AVAILABLE = False

# Fusion 360 (requires bridge add-in)
try:
    from .fusion360 import Fusion360Backend, FUSION360_AVAILABLE
    if FUSION360_AVAILABLE:
        _available_backends["fusion360"] = Fusion360Backend
except ImportError:
    FUSION360_AVAILABLE = False


def get_available_backends():
    """Return dict of available backend names to classes."""
    return _available_backends.copy()


def list_available_backends():
    """Return list of available backend names."""
    return list(_available_backends.keys())


# Lazy imports for backwards compatibility
def get_autocad_backend():
    """Get AutoCAD backend if available."""
    return _available_backends.get("autocad")


def get_solidworks_backend():
    """Get SolidWorks backend if available."""
    return _available_backends.get("solidworks")


def get_fusion360_backend():
    """Get Fusion 360 backend if available."""
    return _available_backends.get("fusion360")


def get_cadquery_backend():
    """Get CadQuery backend if available."""
    return _available_backends.get("cadquery")


def get_freecad_backend():
    """Get FreeCAD backend if available."""
    return _available_backends.get("freecad")


__all__ = [
    "CADBackend",
    "CADObject",
    "CADDocument",
    "Material",
    "get_available_backends",
    "list_available_backends",
    "get_autocad_backend",
    "get_solidworks_backend",
    "get_fusion360_backend",
    "get_cadquery_backend",
    "get_freecad_backend",
]
