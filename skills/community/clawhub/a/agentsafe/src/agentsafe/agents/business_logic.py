"""Business-logic analyst agent."""

from __future__ import annotations

from agentsafe.agents.base import BaseAgent
from agentsafe.llm.prompts import BUSINESS_LOGIC_FOCUS


class BusinessLogicAgent(BaseAgent):
    name = "business_logic"
    focus = BUSINESS_LOGIC_FOCUS
    keywords = (
        "oracle",
        "getprice",
        "pricefeed",
        "swap",
        "slippage",
        "totalSupply",
        "permit",
        "approve",
        "uint256",
        "mint",
        "burn",
        "liquidity",
    )
