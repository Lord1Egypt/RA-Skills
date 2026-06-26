"""DimOS Spec/RPC injection template.

Use a Spec Protocol when one module needs to call methods on another module.
This avoids stringly typed lookups and lets the blueprint fail early when the
required provider is missing.
"""

from __future__ import annotations

from typing import Protocol

from dimos.agents.annotation import skill
from dimos.core.core import rpc
from dimos.core.module import Module
from dimos.spec.utils import Spec


class TargetModuleSpec(Spec, Protocol):
    def perform_action(self, value: float) -> bool: ...


class SkillThatUsesAnotherModule(Module):
    _target: TargetModuleSpec

    @rpc
    def start(self) -> None:
        super().start()

    @rpc
    def stop(self) -> None:
        super().stop()

    @skill
    def agent_action(self, value: float) -> str:
        """Ask the target module to perform a bounded action.

        Args:
            value: Action value. Keep this within the target module's safe range.
        """
        if abs(value) > 1.0:
            return "Refused: value exceeds the safe range for this template."
        ok = self._target.perform_action(value)
        return "Action accepted by target module." if ok else "Target module rejected the action."


skill_that_uses_another_module = SkillThatUsesAnotherModule.blueprint()
