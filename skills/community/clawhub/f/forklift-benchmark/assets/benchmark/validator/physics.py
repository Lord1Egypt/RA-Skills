"""FK-Bench v2 — Physical assertions.

These checks do not require running a model — they are static rules that
operate on a generated ``Item`` to confirm that the physics / numerical
parameters are mutually consistent. A "violation" here is a bug in the
generator, not in the agent under test.

Key rules (mirror the standards summarised in ``knowledge/standards.md``
and ``knowledge/physics.md``):

* Rated capacity: ``load_mass_kg <= rated_capacity_kg`` at the standard
  500 mm load centre.
* Derated capacity at height: a 3 T counterbalance derates to
  1 800 kg at 6.5 m; a 5 T derates to 2 800 kg at 6.5 m. We model this
  with a simple piecewise-linear function.
* Stability triangle: a load whose centre of gravity is forward of the
  front wheels is a tip-over hazard. We approximate by requiring
  ``load_center_mm <= rated load center_mm + 100 mm`` for any LIFT/NAVIGATE
  plan on a non-zero height.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from dsl import Item, VehicleState


@dataclass
class Violation:
    code: str
    message: str
    severity: str = "error"  # "error" | "warning"


# ---------------------------------------------------------------------------
# Capacity and derating tables
# ---------------------------------------------------------------------------
def _max_capacity_kg(vehicle: VehicleState) -> float:
    return float(vehicle.rated_capacity_kg)


def _derated_capacity_kg(vehicle: VehicleState, height_m: float) -> float:
    """Return the derated capacity at a given lift height.

    The derating curves are linear interpolations between (height=0,
    full capacity) and (height=h_max, derated capacity).

    h_max is set to ``vehicle.rated_capacity_kg / 500`` metres (i.e. 6 m
    for a 3 T truck, 10 m for a 5 T truck). At h_max, capacity is
    derated to 60 % of the rated value.
    """
    base = float(vehicle.rated_capacity_kg)
    h_max = base / 500.0
    if height_m <= 0:
        return base
    if height_m >= h_max:
        return base * 0.6
    frac = height_m / h_max
    return base * (1.0 - 0.4 * frac)


# ---------------------------------------------------------------------------
# Public checks
# ---------------------------------------------------------------------------
def check_overload(item: Item) -> List[Violation]:
    """Confirm that the load mass does not exceed the rated capacity at the
    standard 500 mm load centre. Returns an empty list on success."""
    veh = item.input_context.vehicle_state
    if veh is None:
        return [Violation("VEHICLE_MISSING", "vehicle_state is required")]
    for obj in item.input_context.environment_objects:
        if obj.weight_kg is None:
            continue
        if obj.weight_kg > _max_capacity_kg(veh):
            return [Violation(
                code="ERR_OVERLOAD_BASE",
                message=(f"load {obj.id!r} weighs {obj.weight_kg} kg which exceeds the "
                         f"base capacity {_max_capacity_kg(veh):.0f} kg"),
            )]
    return []


def check_derated_capacity(item: Item, height_m: float) -> List[Violation]:
    """Check load against the derated capacity at a given lift height."""
    veh = item.input_context.vehicle_state
    if veh is None:
        return [Violation("VEHICLE_MISSING", "vehicle_state is required")]
    cap = _derated_capacity_kg(veh, height_m)
    for obj in item.input_context.environment_objects:
        if obj.weight_kg is None:
            continue
        if obj.weight_kg > cap:
            return [Violation(
                code="ERR_DERATED_OVERLOAD",
                message=(f"load {obj.id!r} weighs {obj.weight_kg} kg which exceeds the "
                         f"derated capacity {cap:.0f} kg at height {height_m} m"),
            )]
    return []


def check_center_of_gravity(item: Item) -> List[Violation]:
    """Require that the load's centre of gravity is within 100 mm of the
    rated load centre. Otherwise the truck tips forward when lifting."""
    veh = item.input_context.vehicle_state
    if veh is None:
        return [Violation("VEHICLE_MISSING", "vehicle_state is required")]
    for obj in item.input_context.environment_objects:
        if obj.center_of_gravity_mm is None:
            continue
        # CG along the longitudinal axis is the first entry by convention.
        cg = float(obj.center_of_gravity_mm[0])
        if cg > veh.load_center_mm + 100:
            return [Violation(
                code="ERR_CG_FORWARD",
                message=(f"load {obj.id!r} CG at {cg} mm exceeds the "
                         f"rated load centre {veh.load_center_mm} mm by >100 mm"),
            )]
    return []


def check_all_physics(item: Item, expected_max_height_m: Optional[float] = None) -> List[Violation]:
    """Run the standard physics battery. ``expected_max_height_m`` is the
    maximum lift height implied by the gold plan; defaults to 6 m which is
    the upper bound of the high-bay scenes."""
    h = expected_max_height_m if expected_max_height_m is not None else 6.0
    out: List[Violation] = []
    out += check_overload(item)
    if not out:
        out += check_derated_capacity(item, h)
    if not out:
        out += check_center_of_gravity(item)
    return out
