"""Metric screw hole dimensions (pure Python), in mm.

- clearance: ISO 273, medium series.
- tap: tap drill for ISO coarse threads.
- counterbore: seat for ISO 4762 socket head cap screws (DIN 974-1):
  (diameter, depth). Depth = head height + 0.4 mm, so the head sits below the surface.
- countersink: 90 degree seat for ISO 10642 countersunk screws, diameter =
  maximum head diameter + 0.2 mm.
"""

from __future__ import annotations

from typing import Dict, Tuple

CLEARANCE: Dict[str, float] = {
    "M2": 2.4,
    "M2.5": 2.9,
    "M3": 3.4,
    "M4": 4.5,
    "M5": 5.5,
    "M6": 6.6,
    "M8": 9.0,
    "M10": 11.0,
    "M12": 13.5,
    "M14": 15.5,
    "M16": 17.5,
    "M20": 22.0,
}
TAP: Dict[str, float] = {
    "M2": 1.6,
    "M2.5": 2.05,
    "M3": 2.5,
    "M4": 3.3,
    "M5": 4.2,
    "M6": 5.0,
    "M8": 6.8,
    "M10": 8.5,
    "M12": 10.2,
    "M14": 12.0,
    "M16": 14.0,
    "M20": 17.5,
}
COUNTERBORE: Dict[str, Tuple[float, float]] = {
    "M2": (4.3, 2.4),
    "M2.5": (5.0, 2.9),
    "M3": (6.5, 3.4),
    "M4": (8.0, 4.4),
    "M5": (10.0, 5.4),
    "M6": (11.0, 6.4),
    "M8": (15.0, 8.4),
    "M10": (18.0, 10.4),
    "M12": (20.0, 12.4),
    "M14": (24.0, 14.4),
    "M16": (26.0, 16.4),
    "M20": (33.0, 20.4),
}
COUNTERSINK: Dict[str, float] = {
    "M2": 4.6,
    "M2.5": 5.7,
    "M3": 6.9,
    "M4": 9.2,
    "M5": 11.4,
    "M6": 13.7,
    "M8": 18.2,
    "M10": 22.7,
    "M12": 27.2,
    "M14": 31.0,
    "M16": 33.9,
    "M20": 40.6,
}
SIZES = tuple(CLEARANCE)


def hole_dimensions(size: str, fit: str, kind: str) -> Dict[str, float]:
    """Diameter and seat dimensions for a metric screw hole."""
    out = {"diameter": (CLEARANCE if fit == "clearance" else TAP)[size]}
    if kind == "counterbore":
        out["cut_diameter"], out["cut_depth"] = COUNTERBORE[size]
    elif kind == "countersink":
        out["cut_diameter"] = COUNTERSINK[size]
    return out
