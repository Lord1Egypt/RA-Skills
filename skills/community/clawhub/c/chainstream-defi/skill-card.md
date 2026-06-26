## Description: <br>
Execute irreversible on-chain DeFi operations via CLI and MCP tools, including swaps, token launches, transaction signing, broadcasting, and trading workflows that require explicit user confirmation before destructive actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harry5556](https://clawhub.ai/user/harry5556) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to route, prepare, sign, and broadcast DeFi transactions across supported chains while preserving a human review step before irreversible wallet actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide real wallet signing, broadcasting, token creation, swaps, bridges, or paid plan purchases that may be irreversible. <br>
Mitigation: Use a dedicated low-balance wallet and approve any signing, broadcast, token creation, swap, bridge, or paid plan only after reviewing chain, token, amount, recipient, fees, slippage, and route. <br>
Risk: A wallet or sensitive credential may be required for destructive DeFi actions. <br>
Mitigation: Avoid importing a main private key; verify CLI, MCP, SDK, and payment tooling before granting wallet authority. <br>
Risk: Market execution can produce unfavorable outcomes from slippage, price impact, gas costs, stale quotes, or failed transactions. <br>
Mitigation: Follow the quote, confirm, sign, broadcast, and status-check flow; do not auto-retry failed or stale transactions without rebuilding the route and getting fresh confirmation. <br>


## Reference(s): <br>
- [Swap protocol](references/swap-protocol.md) <br>
- [Launchpad](references/launchpad.md) <br>
- [Currency resolution](references/currency-resolution.md) <br>
- [Safety protocol](rules/safety-protocol.md) <br>
- [Execution checklist](rules/execution-checklist.md) <br>
- [Authentication](shared/authentication.md) <br>
- [x402 payment](shared/x402-payment.md) <br>
- [ChainStream MCP server](https://mcp.chainstream.io/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, transaction summaries, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should surface chain, token, amount, route, slippage, fees, confirmation status, transaction hash, and explorer links when applicable.] <br>

## Skill Version(s): <br>
1.1.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
