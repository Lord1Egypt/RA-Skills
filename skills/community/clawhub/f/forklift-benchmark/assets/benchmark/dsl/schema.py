"""FK-Bench v2 — Data schema for benchmark items.

Every JSON file in ``data/v2.0/`` is one ``Item``. The structure mirrors the
example in the project brief. The fields are deliberately simple Python
dataclasses so the package has zero runtime dependencies beyond the
standard library (Pydantic is optional — see ``validate_item_json``).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .actions import ABORT_ACTIONS, Action, ACTION_KINDS


# ---------------------------------------------------------------------------
# Enumerations / constants
# ---------------------------------------------------------------------------
MODULES: Tuple[str, ...] = (
    "MOD-1", "MOD-2", "MOD-3", "MOD-4", "MOD-5", "MOD-6",
)

SCENES: Tuple[str, ...] = (
    "S1_HIGH_BAY",
    "S2_BLOCK",
    "S3_DOCK",
    "S4_LINE_SIDE",
    "S5_VNA",
    "S6_OUTDOOR",
    "S7_MIXED",
)

DIFFICULTIES: Tuple[str, ...] = ("basic", "intermediate", "edge_case")

# The reference distribution grid (counts).
# Module × Difficulty
MOD_DIST: Dict[str, Dict[str, int]] = {
    "MOD-1": {"basic": 32, "intermediate": 36, "edge_case": 12},
    "MOD-2": {"basic": 40, "intermediate": 45, "edge_case": 15},
    "MOD-3": {"basic": 40, "intermediate": 45, "edge_case": 15},
    "MOD-4": {"basic": 36, "intermediate": 40, "edge_case": 14},
    "MOD-5": {"basic": 32, "intermediate": 36, "edge_case": 12},
    "MOD-6": {"basic": 20, "intermediate": 22, "edge_case":  8},
}

# Scene × Difficulty
SCENE_DIST: Dict[str, Dict[str, int]] = {
    "S1_HIGH_BAY":  {"basic": 30, "intermediate": 40, "edge_case": 10},
    "S2_BLOCK":     {"basic": 30, "intermediate": 35, "edge_case": 15},
    "S3_DOCK":      {"basic": 25, "intermediate": 35, "edge_case": 15},
    "S4_LINE_SIDE": {"basic": 30, "intermediate": 40, "edge_case": 15},
    "S5_VNA":       {"basic": 25, "intermediate": 30, "edge_case": 10},
    "S6_OUTDOOR":   {"basic": 20, "intermediate": 30, "edge_case": 10},
    "S7_MIXED":     {"basic": 20, "intermediate": 15, "edge_case": 20},
}

# Module totals
MODULE_COUNTS: Dict[str, int] = {m: sum(d.values()) for m, d in MOD_DIST.items()}
# Scene totals
SCENE_COUNTS: Dict[str, int] = {s: sum(d.values()) for s, d in SCENE_DIST.items()}
# Difficulty totals
DIFFICULTY_COUNTS: Dict[str, int] = {
    "basic": sum(d["basic"] for d in MOD_DIST.values()),
    "intermediate": sum(d["intermediate"] for d in MOD_DIST.values()),
    "edge_case": sum(d["edge_case"] for d in MOD_DIST.values()),
}
TOTAL_ITEMS: int = sum(MODULE_COUNTS.values())  # 500


# ---------------------------------------------------------------------------
# Sub-structures
# ---------------------------------------------------------------------------
@dataclass
class Meta:
    module: str
    scene_type: str
    difficulty: str
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Meta":
        if d["module"] not in MODULES:
            raise ValueError(f"Unknown module: {d['module']!r}")
        if d["scene_type"] not in SCENES:
            raise ValueError(f"Unknown scene: {d['scene_type']!r}")
        if d["difficulty"] not in DIFFICULTIES:
            raise ValueError(f"Unknown difficulty: {d['difficulty']!r}")
        return cls(
            module=d["module"],
            scene_type=d["scene_type"],
            difficulty=d["difficulty"],
            tags=list(d.get("tags", [])),
        )


@dataclass
class VehicleState:
    model_type: str
    rated_capacity_kg: float
    load_center_mm: int
    current_mast_height_m: float = 0.0
    derating_curve_id: str = "DC_STD"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "VehicleState":
        return cls(
            model_type=str(d["model_type"]),
            rated_capacity_kg=float(d["rated_capacity_kg"]),
            load_center_mm=int(d["load_center_mm"]),
            current_mast_height_m=float(d.get("current_mast_height_m", 0.0)),
            derating_curve_id=str(d.get("derating_curve_id", "DC_STD")),
        )


@dataclass
class EnvironmentObject:
    id: str
    type: str
    weight_kg: Optional[float] = None
    dimensions_m: Optional[List[float]] = None
    center_of_gravity_mm: Optional[List[float]] = None
    height_m: Optional[float] = None
    max_load_kg: Optional[float] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["extra"] = dict(self.extra)
        return d

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "EnvironmentObject":
        known = {"id", "type", "weight_kg", "dimensions_m",
                 "center_of_gravity_mm", "height_m", "max_load_kg"}
        extra = {k: v for k, v in d.items() if k not in known}
        return cls(
            id=str(d["id"]),
            type=str(d["type"]),
            weight_kg=(float(d["weight_kg"]) if d.get("weight_kg") is not None else None),
            dimensions_m=(list(d["dimensions_m"]) if d.get("dimensions_m") is not None else None),
            center_of_gravity_mm=(list(d["center_of_gravity_mm"]) if d.get("center_of_gravity_mm") is not None else None),
            height_m=(float(d["height_m"]) if d.get("height_m") is not None else None),
            max_load_kg=(float(d["max_load_kg"]) if d.get("max_load_kg") is not None else None),
            extra=extra,
        )


@dataclass
class InputContext:
    natural_instruction: str
    vehicle_state: VehicleState
    environment_objects: List[EnvironmentObject] = field(default_factory=list)
    sensor_noise: List[str] = field(default_factory=list)
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "natural_instruction": self.natural_instruction,
            "vehicle_state": self.vehicle_state.to_dict(),
            "environment_objects": [o.to_dict() for o in self.environment_objects],
            "sensor_noise": list(self.sensor_noise),
            "extra": dict(self.extra),
        }
        return d

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "InputContext":
        return cls(
            natural_instruction=str(d["natural_instruction"]),
            vehicle_state=VehicleState.from_dict(d["vehicle_state"]),
            environment_objects=[EnvironmentObject.from_dict(o) for o in d.get("environment_objects", [])],
            sensor_noise=list(d.get("sensor_noise", [])),
            extra=dict(d.get("extra", {})),
        )


@dataclass
class ActionPlan:
    expected_decision: str
    action_plan: List[Action] = field(default_factory=list)
    error_code: Optional[str] = None
    rationale: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "expected_decision": self.expected_decision,
            "action_plan": [a.to_dict() for a in self.action_plan],
            "error_code": self.error_code,
            "rationale": self.rationale,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ActionPlan":
        actions = [Action.from_dict(a) for a in d.get("action_plan", [])]
        for a in actions:
            if a.kind not in ACTION_KINDS:
                raise ValueError(f"Unknown action kind: {a.kind!r}")
        return cls(
            expected_decision=str(d["expected_decision"]),
            action_plan=actions,
            error_code=(d.get("error_code") if d.get("error_code") is not None else None),
            rationale=str(d.get("rationale", "")),
        )


@dataclass
class EvalMetrics:
    strict_match_required: bool = False
    allow_partial_credit: bool = True
    red_line_violated: bool = False
    red_line_score: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "EvalMetrics":
        return cls(
            strict_match_required=bool(d.get("strict_match_required", False)),
            allow_partial_credit=bool(d.get("allow_partial_credit", True)),
            red_line_violated=bool(d.get("red_line_violated", False)),
            red_line_score=float(d.get("red_line_score", 1.0)),
        )


@dataclass
class Item:
    item_id: str
    meta: Meta
    input_context: InputContext
    ground_truth: ActionPlan
    eval_metrics: EvalMetrics = field(default_factory=EvalMetrics)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "meta": self.meta.to_dict(),
            "input_context": self.input_context.to_dict(),
            "ground_truth": self.ground_truth.to_dict(),
            "eval_metrics": self.eval_metrics.to_dict(),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Item":
        return cls(
            item_id=str(d["item_id"]),
            meta=Meta.from_dict(d["meta"]),
            input_context=InputContext.from_dict(d["input_context"]),
            ground_truth=ActionPlan.from_dict(d["ground_truth"]),
            eval_metrics=EvalMetrics.from_dict(d.get("eval_metrics", {})),
        )

    def to_json(self, indent: Optional[int] = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    @classmethod
    def from_json(cls, s: str) -> "Item":
        return cls.from_dict(json.loads(s))


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
def validate_item_dict(d: Dict[str, Any]) -> List[str]:
    """Light-weight JSON-shape validator. Returns a list of error strings
    (empty list == item is structurally valid)."""
    errors: List[str] = []
    for key in ("item_id", "meta", "input_context", "ground_truth"):
        if key not in d:
            errors.append(f"missing top-level key: {key!r}")
    if errors:
        return errors
    try:
        Item.from_dict(d)
    except Exception as e:  # noqa: BLE001
        errors.append(f"Item.from_dict failed: {e}")
    return errors


def validate_item_json(path: Path) -> List[str]:
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return [f"json load failed: {e}"]
    return validate_item_dict(d)


# ---------------------------------------------------------------------------
# Helpers used by the generator
# ---------------------------------------------------------------------------
def expected_decision_for(module: str, difficulty: str) -> str:
    """Return the expected_decision string for a (module, difficulty) pair.

    MOD-4 edge cases are HARD safety aborts. Other MOD-4 items still expect
    a cautious plan but the decision is still EXECUTE. The red-line veto in
    the scorer is what enforces the abort when the model fails to emit one.
    """
    if module == "MOD-4" and difficulty == "edge_case":
        return "SAFETY_ABORT"
    return "EXECUTE"


def is_red_line(module: str, difficulty: str) -> bool:
    """A red-line item is one where any wrong execution action (non-abort)
    should be scored 0. We mark MOD-4 edge_case as red-line; in addition,
    a small fraction of MOD-4 intermediate items are also red-line
    (handled by the generator on a per-item basis)."""
    return module == "MOD-4" and difficulty == "edge_case"
