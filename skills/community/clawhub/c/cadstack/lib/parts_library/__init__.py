"""Parametric parts library for CADStack.

This module provides a library of common mechanical parts that can be
instantiated with custom parameters. Parts include fasteners, bearings,
motors, extrusions, and other standard components.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass
import json
import logging

logger = logging.getLogger(__name__)

# Parts library directory
PARTS_DIR = Path(__file__).parent / "data"


@dataclass
class PartDefinition:
    """Definition of a parametric part.

    Attributes:
        name: Part identifier (e.g., "screw_metric")
        category: Part category (e.g., "fasteners")
        description: Human-readable description
        parameters: Dict of parameter name to {type, default, min, max, description}
        generator: Function to create the part
    """
    name: str
    category: str
    description: str
    parameters: Dict[str, Dict[str, Any]]
    generator: Callable


# =============================================================================
# Registry
# =============================================================================

_PART_REGISTRY: Dict[str, PartDefinition] = {}


def register_part(name: str, category: str, description: str):
    """Decorator to register a part generator function."""
    def decorator(func: Callable):
        # Extract parameter info from function signature
        import inspect
        sig = inspect.signature(func)

        parameters = {}
        for param_name, param in sig.parameters.items():
            if param_name in ('backend',):
                continue

            param_info = {
                "type": "float",
                "description": param_name.replace("_", " ").title(),
            }

            if param.default != inspect.Parameter.empty:
                param_info["default"] = param.default

            parameters[param_name] = param_info

        part_def = PartDefinition(
            name=name,
            category=category,
            description=description,
            parameters=parameters,
            generator=func
        )
        _PART_REGISTRY[name] = part_def

        return func
    return decorator


def get_part_definition(name: str) -> Optional[PartDefinition]:
    """Get a part definition by name."""
    return _PART_REGISTRY.get(name)


def list_parts(category: Optional[str] = None) -> List[str]:
    """List available part names, optionally filtered by category."""
    if category:
        return [name for name, part in _PART_REGISTRY.items()
                if part.category == category]
    return list(_PART_REGISTRY.keys())


def list_categories() -> List[str]:
    """List all part categories."""
    return sorted(set(part.category for part in _PART_REGISTRY.values()))


def create_part(name: str, backend: Any, **kwargs) -> Any:
    """Create a part instance.

    Args:
        name: Part name
        backend: CAD backend to use
        **kwargs: Part parameters

    Returns:
        Created CAD object

    Raises:
        ValueError: If part not found or invalid parameters
    """
    part_def = _PART_REGISTRY.get(name)
    if part_def is None:
        raise ValueError(f"Part '{name}' not found. Available: {list_parts()}")

    # Validate parameters
    for param_name, param_info in part_def.parameters.items():
        if param_name not in kwargs and "default" not in param_info:
            raise ValueError(f"Missing required parameter: {param_name}")

    # Apply defaults
    for param_name, param_info in part_def.parameters.items():
        if param_name not in kwargs:
            kwargs[param_name] = param_info["default"]

    logger.info(f"Creating part '{name}' with params: {kwargs}")
    return part_def.generator(backend, **kwargs)


# =============================================================================
# Fasteners
# =============================================================================

@register_part("screw_metric", "fasteners", "Metric cap head screw (DIN 912)")
def screw_metric(backend, diameter: float = 3.0, length: float = 10.0) -> Any:
    """Create a metric cap head screw.

    Args:
        backend: CAD backend
        diameter: Thread diameter in mm (M3, M4, M5, etc.)
        length: Screw length in mm

    Returns:
        CAD object representing the screw
    """
    # Standard dimensions for metric cap screws
    head_diameter = diameter * 2.0
    head_height = diameter * 0.7
    socket_diameter = diameter * 0.5
    socket_depth = diameter * 0.4

    # Create head (cylinder with hex socket)
    head = backend.create_cylinder(head_diameter / 2, head_height, "screw_head")

    # Create socket (hexagonal recess - approximated as cylinder for simplicity)
    socket = backend.create_cylinder(socket_diameter / 2, socket_depth, "socket")
    socket = backend.move(socket, 0, 0, head_height - socket_depth)

    # Subtract socket from head
    head_with_socket = backend.cut(head, socket, "head_with_socket")

    # Create shank
    shank = backend.create_cylinder(diameter / 2, length, "shank")
    shank = backend.move(shank, 0, 0, head_height)

    # Union head and shank
    screw = backend.fuse(head_with_socket, shank, f"screw_M{int(diameter)}x{int(length)}")

    return screw


@register_part("nut_hex", "fasteners", "Hexagonal nut (DIN 934)")
def nut_hex(backend, diameter: float = 3.0) -> Any:
    """Create a hexagonal nut.

    Args:
        backend: CAD backend
        diameter: Thread diameter in mm

    Returns:
        CAD object representing the nut
    """
    import math

    # Standard dimensions
    width_across_flats = diameter * 1.8  # Wrench size
    height = diameter * 0.8

    # Create hexagonal prism (approximate with filleted box for now)
    # For true hexagon, we'd need polygon support
    radius = width_across_flats / 2

    # Create cylinder and cut to hexagon shape
    hex_outer = backend.create_cylinder(radius, height, "hex_outer")

    # Create through hole
    hole = backend.create_cylinder(diameter / 2, height, "hole")

    # Subtract hole
    nut = backend.cut(hex_outer, hole, f"nut_M{int(diameter)}")

    return nut


@register_part("washer", "fasteners", "Flat washer (DIN 125)")
def washer(backend, diameter: float = 3.0) -> Any:
    """Create a flat washer.

    Args:
        backend: CAD backend
        diameter: Bolt diameter in mm

    Returns:
        CAD object representing the washer
    """
    # Standard dimensions
    outer_diameter = diameter * 2.0
    inner_diameter = diameter * 1.1
    thickness = diameter * 0.2

    # Create outer cylinder
    outer = backend.create_cylinder(outer_diameter / 2, thickness, "washer_outer")

    # Create inner hole
    hole = backend.create_cylinder(inner_diameter / 2, thickness, "washer_hole")

    # Subtract
    washer = backend.cut(outer, hole, f"washer_M{int(diameter)}")

    return washer


# =============================================================================
# Bearings
# =============================================================================

@register_part("bearing_608", "bearings", "608 series skate bearing")
def bearing_608(backend) -> Any:
    """Create a 608 skate bearing (standard skateboard bearing).

    Dimensions: 22mm OD x 8mm ID x 7mm width
    """
    outer_od = 22.0
    inner_id = 8.0
    width = 7.0

    # Outer race
    outer = backend.create_cylinder(outer_od / 2, width, "outer_race")

    # Inner race
    inner = backend.create_cylinder(inner_id / 2, width, "inner_race")

    # Subtract inner from outer (simplified - real bearing has ball groove)
    bearing = backend.cut(outer, inner, "bearing_608")

    return bearing


@register_part("bearing_625", "bearings", "625 series radial bearing")
def bearing_625(backend) -> Any:
    """Create a 625 radial bearing.

    Dimensions: 16mm OD x 5mm ID x 5mm width
    """
    outer_od = 16.0
    inner_id = 5.0
    width = 5.0

    outer = backend.create_cylinder(outer_od / 2, width, "outer_race")
    inner = backend.create_cylinder(inner_id / 2, width, "inner_race")
    bearing = backend.cut(outer, inner, "bearing_625")

    return bearing


@register_part("bearing_6800", "bearings", "6800 series thin section bearing")
def bearing_6800(backend, size_code: int = 0) -> Any:
    """Create a 6800 series thin section bearing.

    Args:
        backend: CAD backend
        size_code: Size code (0-9, e.g., 0 = 6800, 1 = 6801, etc.)
    """
    # Common 6800 series dimensions
    dimensions = {
        0: (19, 10, 5),   # 6800: 19x10x5
        1: (21, 12, 5),   # 6801
        2: (24, 15, 5),   # 6802
        3: (26, 17, 5),   # 6803
        4: (28, 19, 5),   # 6804
        5: (32, 25, 7),   # 6805
        6: (37, 30, 7),   # 6806
        7: (42, 35, 7),   # 6807
        8: (47, 40, 7),   # 6808
        9: (52, 45, 7),   # 6809
    }

    if size_code not in dimensions:
        raise ValueError(f"Invalid size code: {size_code}. Valid: 0-9")

    od, id_, width = dimensions[size_code]

    outer = backend.create_cylinder(od / 2, width, "outer")
    inner = backend.create_cylinder(id_ / 2, width, "inner")
    bearing = backend.cut(outer, inner, f"bearing_680{size_code}")

    return bearing


# =============================================================================
# Motors
# =============================================================================

@register_part("nema17_motor", "motors", "NEMA 17 stepper motor")
def nema17_motor(backend, length: float = 40.0) -> Any:
    """Create a NEMA 17 stepper motor model.

    Args:
        backend: CAD backend
        length: Motor body length in mm (typically 34-48mm)

    Returns:
        CAD object representing the motor
    """
    # NEMA 17 standard dimensions
    frame_size = 42.3  # Frame width/height
    shaft_diameter = 5.0
    shaft_length = 24.0
    mounting_hole_distance = 31.0  # Distance between mounting holes
    mounting_hole_diameter = 3.0

    # Create main body
    body = backend.create_box(frame_size, frame_size, length, "motor_body")

    # Create shaft protrusion (on top)
    shaft = backend.create_cylinder(shaft_diameter / 2, shaft_length, "shaft")
    shaft = backend.move(shaft, 0, 0, length)
    motor = backend.fuse(body, shaft, "nema17_motor")

    return motor


@register_part("nema23_motor", "motors", "NEMA 23 stepper motor")
def nema23_motor(backend, length: float = 76.0) -> Any:
    """Create a NEMA 23 stepper motor model.

    Args:
        backend: CAD backend
        length: Motor body length in mm

    Returns:
        CAD object representing the motor
    """
    # NEMA 23 standard dimensions
    frame_size = 57.0
    shaft_diameter = 6.35
    shaft_length = 30.0

    body = backend.create_box(frame_size, frame_size, length, "motor_body")
    shaft = backend.create_cylinder(shaft_diameter / 2, shaft_length, "shaft")
    shaft = backend.move(shaft, 0, 0, length)
    motor = backend.fuse(body, shaft, "nema23_motor")

    return motor


# =============================================================================
# Extrusions
# =============================================================================

@register_part("extrusion_2020", "extrusions", "2020 aluminum T-slot extrusion")
def extrusion_2020(backend, length: float = 100.0) -> Any:
    """Create a 2020 T-slot extrusion profile.

    Args:
        backend: CAD backend
        length: Extrusion length in mm

    Returns:
        CAD object representing the extrusion
    """
    # 2020 dimensions
    width = 20.0
    height = 20.0
    slot_width = 5.0
    slot_depth = 6.0

    # Create main profile (simplified as box for now)
    extrusion = backend.create_box(width, height, length, "extrusion_2020")

    return extrusion


@register_part("extrusion_2040", "extrusions", "2040 aluminum T-slot extrusion")
def extrusion_2040(backend, length: float = 100.0) -> Any:
    """Create a 2040 T-slot extrusion profile.

    Args:
        backend: CAD backend
        length: Extrusion length in mm

    Returns:
        CAD object representing the extrusion
    """
    # 2040 dimensions (2x 2020 side by side)
    width = 40.0
    height = 20.0

    extrusion = backend.create_box(width, height, length, "extrusion_2040")

    return extrusion


@register_part("extrusion_4040", "extrusions", "4040 aluminum T-slot extrusion")
def extrusion_4040(backend, length: float = 100.0) -> Any:
    """Create a 4040 T-slot extrusion profile.

    Args:
        backend: CAD backend
        length: Extrusion length in mm

    Returns:
        CAD object representing the extrusion
    """
    # 4040 dimensions
    width = 40.0
    height = 40.0

    extrusion = backend.create_box(width, height, length, "extrusion_4040")

    return extrusion


# =============================================================================
# Standoffs and Spacers
# =============================================================================

@register_part("standoff_hex", "standoffs", "Hexagonal standoff")
def standoff_hex(backend, diameter: float = 6.0, length: float = 20.0,
                 hole_diameter: float = 3.0) -> Any:
    """Create a hexagonal standoff.

    Args:
        backend: CAD backend
        diameter: Outer diameter in mm
        length: Standoff length in mm
        hole_diameter: Through hole diameter in mm

    Returns:
        CAD object representing the standoff
    """
    # Create hex body (approximated as cylinder)
    body = backend.create_cylinder(diameter / 2, length, "standoff_body")

    # Create through hole
    hole = backend.create_cylinder(hole_diameter / 2, length, "hole")

    # Subtract
    standoff = backend.cut(body, hole, "standoff_hex")

    return standoff


# =============================================================================
# Load saved part definitions from JSON
# =============================================================================

def _load_parts_from_json():
    """Load part definitions from JSON files in data directory."""
    if not PARTS_DIR.exists():
        return

    for json_file in PARTS_DIR.glob("*.json"):
        try:
            with open(json_file) as f:
                data = json.load(f)

            for part_name, part_def in data.items():
                # Store metadata for lookup (actual generation requires code)
                if "parameters" in part_def:
                    logger.debug(f"Loaded part definition: {part_name}")
        except Exception as e:
            logger.warning(f"Failed to load {json_file}: {e}")


# Initialize
_load_parts_from_json()


# =============================================================================
# Public API
# =============================================================================

__all__ = [
    "register_part",
    "get_part_definition",
    "list_parts",
    "list_categories",
    "create_part",
    "PARTS_DIR",
]
