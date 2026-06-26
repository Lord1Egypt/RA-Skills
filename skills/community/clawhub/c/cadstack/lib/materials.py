"""Material properties database for CAD objects.

This module provides material definitions with density values
for mass calculations, as well as visual properties for rendering.
"""

from dataclasses import dataclass
from typing import Dict, Optional, List
import logging

from .backends.base import Material

logger = logging.getLogger(__name__)


# =============================================================================
# Material Database
# =============================================================================

MATERIALS: Dict[str, Material] = {
    # Aluminum alloys
    "aluminum_6061": Material(
        name="aluminum_6061",
        density=2.70,  # g/cm³
        color="#A8A9AD",
        description="6061-T6 Aluminum alloy, general purpose"
    ),
    "aluminum_6063": Material(
        name="aluminum_6063",
        density=2.70,
        color="#C0C0C0",
        description="6063 Aluminum architectural alloy"
    ),
    "aluminum_7075": Material(
        name="aluminum_7075",
        density=2.81,
        color="#A8A9AD",
        description="7075-T6 Aluminum, high strength"
    ),

    # Steel alloys
    "steel_1018": Material(
        name="steel_1018",
        density=7.87,
        color="#71797E",
        description="1018 Mild steel, general purpose"
    ),
    "steel_4140": Material(
        name="steel_4140",
        density=7.85,
        color="#71797E",
        description="4140 Alloy steel, high strength"
    ),
    "steel_304": Material(
        name="steel_304",
        density=8.00,
        color="#B8B8B8",
        description="304 Stainless steel"
    ),
    "steel_316": Material(
        name="steel_316",
        density=8.03,
        color="#B8B8B8",
        description="316 Stainless steel, marine grade"
    ),

    # Other metals
    "brass": Material(
        name="brass",
        density=8.50,
        color="#B5A642",
        description="Yellow brass"
    ),
    "copper": Material(
        name="copper",
        density=8.96,
        color="#B87333",
        description="Pure copper"
    ),
    "titanium": Material(
        name="titanium",
        density=4.51,
        color="#878681",
        description="Ti-6Al-4V Titanium alloy"
    ),
    "magnesium": Material(
        name="magnesium",
        density=1.74,
        color="#E5E4E2",
        description="Magnesium alloy"
    ),

    # Plastics
    "abs_plastic": Material(
        name="abs_plastic",
        density=1.07,
        color="#2C2C2C",
        description="ABS plastic, black"
    ),
    "pla_plastic": Material(
        name="pla_plastic",
        density=1.25,
        color="#FFFFFF",
        description="PLA plastic for 3D printing"
    ),
    "petg_plastic": Material(
        name="petg_plastic",
        density=1.27,
        color="#FFFFFF",
        description="PETG plastic for 3D printing"
    ),
    "nylon": Material(
        name="nylon",
        density=1.15,
        color="#F5F5F5",
        description="Nylon 6/6"
    ),
    "delrin": Material(
        name="delrin",
        density=1.42,
        color="#FFFFFF",
        description="Delrin/POM acetal"
    ),
    "peek": Material(
        name="peek",
        density=1.32,
        color="#D4AF37",
        description="PEEK high-performance plastic"
    ),

    # Woods (approximate)
    "pine": Material(
        name="pine",
        density=0.51,
        color="#DEB887",
        description="Pine wood (average)"
    ),
    "oak": Material(
        name="oak",
        density=0.75,
        color="#8B4513",
        description="Oak wood (average)"
    ),
    "maple": Material(
        name="maple",
        density=0.63,
        color="#FFE4B5",
        description="Maple wood (average)"
    ),

    # Other materials
    "glass": Material(
        name="glass",
        density=2.50,
        color="#E0FFFF",
        description="Soda-lime glass"
    ),
    "rubber": Material(
        name="rubber",
        density=1.10,
        color="#2C2C2C",
        description="Natural rubber"
    ),
    "ceramic": Material(
        name="ceramic",
        density=2.40,
        color="#F5F5DC",
        description="Technical ceramic"
    ),
}


def get_material(name: str) -> Optional[Material]:
    """Get a material by name.

    Args:
        name: Material name (case-insensitive)

    Returns:
        Material object or None if not found
    """
    # Normalize name
    name_lower = name.lower().replace("-", "_").replace(" ", "_")

    # Direct lookup
    if name_lower in MATERIALS:
        return MATERIALS[name_lower]

    # Try with common prefixes/suffixes
    aliases = {
        "aluminum": "aluminum_6061",
        "aluminium": "aluminum_6061",
        "steel": "steel_1018",
        "stainless": "steel_304",
        "stainless_steel": "steel_304",
        "ss": "steel_304",
        "abs": "abs_plastic",
        "plastic": "abs_plastic",
    }

    if name_lower in aliases:
        return MATERIALS.get(aliases[name_lower])

    return None


def list_materials() -> List[str]:
    """List all available material names."""
    return sorted(MATERIALS.keys())


def search_materials(query: str) -> List[Material]:
    """Search for materials matching a query.

    Args:
        query: Search term

    Returns:
        List of matching materials
    """
    query_lower = query.lower()
    matches = []

    for material in MATERIALS.values():
        if (query_lower in material.name.lower() or
            query_lower in material.description.lower()):
            matches.append(material)

    return matches


def calculate_mass(volume_mm3: float, material_name: str) -> Optional[float]:
    """Calculate mass from volume and material.

    Args:
        volume_mm3: Volume in cubic millimeters
        material_name: Material name

    Returns:
        Mass in grams, or None if material not found
    """
    material = get_material(material_name)
    if material is None:
        return None

    # Convert mm³ to cm³ (divide by 1000)
    volume_cm3 = volume_mm3 / 1000.0

    # Mass = density × volume (g)
    return volume_cm3 * material.density


# =============================================================================
# Material API for CLI
# =============================================================================

def show_material_info(material_name: str) -> str:
    """Get formatted info string for a material."""
    material = get_material(material_name)

    if material is None:
        return f"Material '{material_name}' not found"

    lines = [
        f"Material: {material.name}",
        f"  Density: {material.density} g/cm³",
        f"  Color: {material.color}",
        f"  Description: {material.description}",
    ]
    return "\n".join(lines)


def estimate_mass_string(volume_mm3: float, material_name: str) -> str:
    """Get formatted mass estimate string."""
    mass = calculate_mass(volume_mm3, material_name)

    if mass is None:
        return f"Cannot calculate mass - material '{material_name}' not found"

    if mass < 1000:
        return f"Estimated mass: {mass:.2f} g"
    else:
        return f"Estimated mass: {mass/1000:.2f} kg ({mass:.0f} g)"
