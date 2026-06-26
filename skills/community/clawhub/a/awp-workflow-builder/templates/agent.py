from __future__ import annotations

from typing import Any, Dict

from awp.agent import AWPAgent


class Agent(AWPAgent):
    """{{AGENT_DESCRIPTION}}"""

    @property
    def name(self) -> str:
        return "{{AGENT_ID}}"

    def run(self, task: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent.

        Override for custom logic. When using WorkflowRunner,
        the runtime handles LLM calls, prompt assembly, and
        response parsing automatically.
        """
        state = state or {}
        return {self.name: {"result": "default", "confidence": 0.0}}
