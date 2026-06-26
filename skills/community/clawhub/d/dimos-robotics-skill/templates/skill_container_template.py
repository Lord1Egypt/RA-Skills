"""Minimal DimOS skill container template.

Copy this file into a DimOS package, rename the class, add real logic, then
include the container's blueprint in an MCP-enabled DimOS blueprint.
"""

from __future__ import annotations

from dimos.agents.annotation import skill
from dimos.core.core import rpc
from dimos.core.module import Module


class ExampleSkillContainer(Module):
    """Container for agent-callable DimOS skills."""

    @rpc
    def start(self) -> None:
        super().start()

    @rpc
    def stop(self) -> None:
        super().stop()

    @skill
    def report_status(self) -> str:
        """Report that this skill container is loaded and ready."""
        return "ExampleSkillContainer is loaded and ready."

    @skill
    def echo_labeled_value(self, label: str, value: float) -> str:
        """Echo a labeled numeric value for testing MCP argument passing.

        Args:
            label: Human-readable label for the value.
            value: Numeric value to echo.
        """
        clean_label = label.strip() or "value"
        return f"{clean_label}: {value}"


example_skill_container = ExampleSkillContainer.blueprint()
