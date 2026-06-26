"""Safe DimOS movement wrapper template.

This is a conservative example for wrapping an existing relative-move provider.
It refuses out-of-bounds movement instead of silently executing a capped command.
Start in replay or simulation before trying real hardware.
"""

from __future__ import annotations

from typing import Protocol

from dimos.agents.annotation import skill
from dimos.core.core import rpc
from dimos.core.module import Module
from dimos.spec.utils import Spec


class RelativeMoveSpec(Spec, Protocol):
    """Protocol for a module that can move the robot relative to its pose."""

    def relative_move(
        self,
        forward: float = 0.0,
        left: float = 0.0,
        degrees: float = 0.0,
    ) -> str: ...


class SafeMotionSkill(Module):
    """Agent-callable movement skills with conservative safety limits."""

    _motion: RelativeMoveSpec
    max_forward_m: float = 0.30
    max_left_m: float = 0.20
    max_turn_degrees: float = 20.0

    @rpc
    def start(self) -> None:
        super().start()

    @rpc
    def stop(self) -> None:
        super().stop()

    @skill
    def configure_safe_motion_limits(
        self,
        max_forward_m: float = 0.30,
        max_left_m: float = 0.20,
        max_turn_degrees: float = 20.0,
    ) -> str:
        """Set conservative per-command movement limits for this skill container.

        Args:
            max_forward_m: Maximum absolute forward/backward distance in meters.
            max_left_m: Maximum absolute left/right distance in meters.
            max_turn_degrees: Maximum absolute turn angle in degrees.
        """
        if max_forward_m <= 0 or max_left_m <= 0 or max_turn_degrees <= 0:
            return "Refused: all movement limits must be positive."
        if max_forward_m > 1.0 or max_left_m > 1.0 or max_turn_degrees > 90.0:
            return "Refused: requested limits are too large for a safe default wrapper."

        self.max_forward_m = max_forward_m
        self.max_left_m = max_left_m
        self.max_turn_degrees = max_turn_degrees
        return (
            "Safe motion limits updated: "
            f"forward={self.max_forward_m} m, "
            f"left={self.max_left_m} m, "
            f"turn={self.max_turn_degrees} degrees."
        )

    @skill
    def safe_relative_move(
        self,
        forward: float = 0.0,
        left: float = 0.0,
        degrees: float = 0.0,
    ) -> str:
        """Move the robot a small relative amount after validating safety limits.

        Args:
            forward: Forward/backward distance in meters. Positive is forward.
            left: Left/right distance in meters. Positive is left.
            degrees: Turn in degrees. Positive is counterclockwise.
        """
        if abs(forward) > self.max_forward_m:
            return f"Refused: forward={forward} exceeds limit {self.max_forward_m}."
        if abs(left) > self.max_left_m:
            return f"Refused: left={left} exceeds limit {self.max_left_m}."
        if abs(degrees) > self.max_turn_degrees:
            return f"Refused: degrees={degrees} exceeds limit {self.max_turn_degrees}."
        if forward == 0.0 and left == 0.0 and degrees == 0.0:
            return "No movement requested."

        result = self._motion.relative_move(forward=forward, left=left, degrees=degrees)
        return f"Safe relative move requested. Underlying result: {result}"


safe_motion_skill = SafeMotionSkill.blueprint()
