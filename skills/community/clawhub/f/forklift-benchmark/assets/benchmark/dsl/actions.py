"""FK-Bench v2 — Action DSL.

Defines the 15 primitive actions an embodied forklift agent can emit. Each
action is a structured (kind, params) pair. `ABORT_ACTIONS` are the three
"safety abort" actions that the scorer treats as terminal (they end a plan
without scoring the rest of the sequence). `MOVE_ACTIONS` are the actions
that carry a spatial pose and therefore participate in parameter IoU.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# 15 动作 DSL ---------------------------------------------------------------
ACTION_KINDS: List[str] = [
    "NAVIGATE",          # Move the truck to (to_x, to_y) at max_speed_mps
    "LIFT",              # Raise mast to to_height_m
    "LOWER",             # Lower mast to to_height_m
    "TILT_FORWARD",      # Tilt mast forward to to_deg degrees
    "TILT_BACK",         # Tilt mast back to to_deg degrees
    "SIDESHIFT",         # Sideshift attachment by offset_mm
    "CLAMP",             # Close clamp / squeeze load
    "RELEASE",           # Open clamp / release load
    "ROTATE_CARGO",      # Rotate rotator attachment to to_deg
    "FORK_ADJUST",       # Adjust fork width to width_mm
    "TRAVERSE",          # Move fork carriage depth_m (positive = forward)
    "HORN",              # Sound horn with pattern
    "EMERGENCY_STOP",    # Hard stop — terminates the plan
    "RAISE_ALARM",       # Operator/HMI alarm with channel + code
    "ASK_CLARIFICATION", # Ask the human a clarification question
]

# 红线/安全终止动作
ABORT_ACTIONS: List[str] = ["EMERGENCY_STOP", "RAISE_ALARM", "ASK_CLARIFICATION"]

# 携带空间位姿/物理参数参与 IoU 打分的动作
MOVE_ACTIONS: List[str] = [
    "NAVIGATE",          # (to_x, to_y)
    "LIFT",              # (to_height_m)
    "LOWER",             # (to_height_m)
    "TILT_FORWARD",      # (to_deg)
    "TILT_BACK",         # (to_deg)
    "SIDESHIFT",         # (offset_mm)
    "ROTATE_CARGO",      # (to_deg)
    "FORK_ADJUST",       # (width_mm)
    "TRAVERSE",          # (depth_m)
]

# 每个动作的"主参数"键（用于打分的容差比较）
PRIMARY_PARAM: Dict[str, str] = {
    "NAVIGATE": "to_xy",         # 特殊：二维 (to_x, to_y)
    "LIFT": "to_height_m",
    "LOWER": "to_height_m",
    "TILT_FORWARD": "to_deg",
    "TILT_BACK": "to_deg",
    "SIDESHIFT": "offset_mm",
    "CLAMP": "force_n",
    "RELEASE": "force_n",
    "ROTATE_CARGO": "to_deg",
    "FORK_ADJUST": "width_mm",
    "TRAVERSE": "depth_m",
    "HORN": "pattern",
    "EMERGENCY_STOP": "reason",
    "RAISE_ALARM": "code",
    "ASK_CLARIFICATION": "question",
}


@dataclass
class Action:
    """A single DSL action emitted by the agent under test."""

    kind: str
    params: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {"kind": self.kind, "params": dict(self.params)}

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Action":
        kind = d.get("kind")
        params = dict(d.get("params", {}))
        if kind not in ACTION_KINDS:
            raise ValueError(f"Unknown action kind: {kind!r}")
        return cls(kind=kind, params=params)

    def is_abort(self) -> bool:
        return self.kind in ABORT_ACTIONS

    def is_move(self) -> bool:
        return self.kind in MOVE_ACTIONS


def make_action(kind: str, **params: Any) -> Action:
    """Convenience builder that validates the kind."""
    if kind not in ACTION_KINDS:
        raise ValueError(f"Unknown action kind: {kind!r}")
    return Action(kind=kind, params=params)


# ---------------------------------------------------------------------------
# Shortcut builders (one per kind). Use these to keep generator code terse
# and consistent with the DSL.
# ---------------------------------------------------------------------------
def navigate(to_x: float, to_y: float, max_speed_mps: float = 1.5) -> Action:
    return make_action("NAVIGATE", to_x=float(to_x), to_y=float(to_y), max_speed_mps=float(max_speed_mps))


def lift(to_height_m: float) -> Action:
    return make_action("LIFT", to_height_m=float(to_height_m))


def lower(to_height_m: float) -> Action:
    return make_action("LOWER", to_height_m=float(to_height_m))


def tilt_forward(to_deg: float) -> Action:
    return make_action("TILT_FORWARD", to_deg=float(to_deg))


def tilt_back(to_deg: float) -> Action:
    return make_action("TILT_BACK", to_deg=float(to_deg))


def sideshift(offset_mm: float) -> Action:
    return make_action("SIDESHIFT", offset_mm=float(offset_mm))


def clamp(force_n: float = 2000.0) -> Action:
    return make_action("CLAMP", force_n=float(force_n))


def release(force_n: float = 0.0) -> Action:
    return make_action("RELEASE", force_n=float(force_n))


def rotate_cargo(to_deg: float) -> Action:
    return make_action("ROTATE_CARGO", to_deg=float(to_deg))


def fork_adjust(width_mm: float) -> Action:
    return make_action("FORK_ADJUST", width_mm=float(width_mm))


def traverse(depth_m: float) -> Action:
    return make_action("TRAVERSE", depth_m=float(depth_m))


def horn(pattern: str = "short") -> Action:
    if pattern not in {"short", "long", "continuous"}:
        raise ValueError(f"Invalid horn pattern: {pattern!r}")
    return make_action("HORN", pattern=pattern)


def emergency_stop(reason: str = "") -> Action:
    return make_action("EMERGENCY_STOP", reason=str(reason))


def raise_alarm(channel: str = "operator", code: str = "E_SAFETY") -> Action:
    return make_action("RAISE_ALARM", channel=str(channel), code=str(code))


def ask_clarification(question: str = "") -> Action:
    return make_action("ASK_CLARIFICATION", question=str(question))
