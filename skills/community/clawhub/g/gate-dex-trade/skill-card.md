## Description: <br>
Gate DEX Trade helps agents execute on-chain token swaps, buys, sells, exchanges, conversions, and cross-chain bridge transactions through Gate DEX workflows that require user confirmation and transaction signing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route agent-assisted Gate DEX trades, obtain quotes, prepare swap transactions, complete confirmation steps, sign transactions, and track swap status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-assisted crypto trading can move real funds and requires transaction signing. <br>
Mitigation: Review every trading pair, quote, slippage setting, recipient address, and signature authorization before approving a transaction. <br>
Risk: The security review flags handling of raw wallet keys, persistent credentials, and broad trading-tool configuration as requiring user review. <br>
Mitigation: Prefer MCP wallet signing, do not paste raw private keys or expose .env or keystore files to the agent, replace default API credentials before OpenAPI use, and review installer-created files before using real funds. <br>


## Reference(s): <br>
- [Gate DEX Trade skill page](https://clawhub.ai/gate-exchange/gate-dex-trade) <br>
- [MCP trading workflow](references/mcp.md) <br>
- [OpenAPI trading workflow](references/openapi.md) <br>
- [MCP server setup](references/setup.md) <br>
- [Gate runtime rules](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md) <br>
- [Gate MCP](https://github.com/gate/gate-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with tool-call parameters, transaction confirmation prompts, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include swap quotes, signing prompts, check-in responses, submitted transaction identifiers, and transaction status summaries.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter version 2026.4.2-1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
