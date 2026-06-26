from __future__ import annotations

from typing import Any, Dict

from awp.agent import AWPAgent


class Agent(AWPAgent):
    """AWP agent: {{AGENT_ID}}."""

    @property
    def name(self) -> str:
        return "{{AGENT_ID}}"

    def run(self, task: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent.

        When using WorkflowRunner (awp.runtime), this method is not
        called directly -- the runner uses StandaloneAgent which reads
        agent.awp.yaml and handles LLM calls automatically.

        Override this method for custom agent logic beyond the
        standard prompt-LLM-parse cycle.
        """
        state = state or {}
        return {self.name: {"result": "default", "confidence": 0.0}}
