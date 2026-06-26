## Description: <br>
Facilitates over-the-counter token trades between agents using Uniswap for price discovery and settlement, with ERC-8004 counterparty verification and optional cross-chain intents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent developers use this skill to prepare and execute counterparty-specific token trades, verify agent identity, compare negotiated terms against Uniswap pool pricing, and settle confirmed trades on chain. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prepare and submit Uniswap-based crypto trades, which may cause irreversible financial loss if the counterparty, token, amount, chain, price, slippage, fees, approvals, or transaction details are wrong. <br>
Mitigation: Use a limited wallet and require explicit review of counterparty identity, trade terms, wallet approvals, safety checks, and final transaction details before confirming settlement. <br>
Risk: Trade logs may contain sensitive counterparty, terms, settlement, and transaction information. <br>
Mitigation: Treat trade records as sensitive until the publisher documents where logs are stored, who can access them, and how long they are retained. <br>
Risk: Cross-chain OTC settlement can add bridge or intent latency and may fail due to liquidity, gas, chain, or bridge conditions. <br>
Mitigation: Confirm source and destination chains, expected timing, bridge or intent status, gas availability, and fallback behavior before submitting cross-chain trades. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/agent-otc-trade) <br>
- [Publisher profile](https://clawhub.ai/user/wpank) <br>
- [Agentic Uniswap skill source](https://github.com/wpank/Agentic-Uniswap/tree/main/.ai/skills/agent-otc-trade) <br>
- [Agentic Uniswap MCP server](https://github.com/wpank/Agentic-Uniswap/tree/main/packages/mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text trade workflow guidance with transaction details, verification reports, confirmations, and error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Uniswap MCP tools for quotes, prices, pool data, balances, swaps, cross-chain intents, and safety status checks.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
