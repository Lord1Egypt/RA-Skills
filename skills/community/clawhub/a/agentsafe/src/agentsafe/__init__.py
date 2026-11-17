"""agentSAFE MCP - EVM smart contract audit MCP server.

E-version scope: Ethereum Mainnet only. AI-assisted risk screening,
NOT a formal security audit. Absence of findings never means "safe".
"""

from typing import Final

__version__ = "0.1.0"

CHAIN_ID: Final = "ethereum-mainnet"

REPORT_DISCLAIMER = (
    "This report is AI-assisted risk screening, not a formal security audit. "
    "Absence of findings does not mean the contract is safe. "
    "All findings marked tool_detected/llm_suggested require verification before action."
)
