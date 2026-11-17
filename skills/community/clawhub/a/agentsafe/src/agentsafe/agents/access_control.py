"""Access-control analyst agent."""

from __future__ import annotations

from agentsafe.agents.base import BaseAgent
from agentsafe.llm.prompts import ACCESS_CONTROL_FOCUS


class AccessControlAgent(BaseAgent):
    name = "access_control"
    focus = ACCESS_CONTROL_FOCUS
    # Keywords only gate deep-vs-basic prompting; absence proves nothing.
    keywords = (
        "onlyowner",
        "onlyrole",
        "hasrole",
        "grantrole",
        "renounceownership",
        "transferownership",
        "initializer",
        "upgrade",
        "admin",
        "authorizer",
    )
