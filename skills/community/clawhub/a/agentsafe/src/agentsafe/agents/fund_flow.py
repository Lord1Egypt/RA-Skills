"""Fund-flow analyst agent."""

from __future__ import annotations

from agentsafe.agents.base import BaseAgent
from agentsafe.llm.prompts import FUND_FLOW_FOCUS


class FundFlowAgent(BaseAgent):
    name = "fund_flow"
    focus = FUND_FLOW_FOCUS
    keywords = (
        "call.value",
        ".transfer(",
        ".send(",
        "payable",
        "withdraw",
        "deposit",
        "balanceof",
        "weth",
        "ethers",
        "msg.value",
        "safeTransfer",
    )
