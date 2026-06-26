## Description: <br>
Agent-native payments via 1ly MCP for x402 payment handling, USDC payments, paid API access, store and paid-link creation, marketplace search, key management, and token launch, trade, and fee-claim workflows on Solana and Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1lystore](https://clawhub.ai/user/1lystore) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to configure agents for buying paid APIs, accepting USDC payments, creating paid links or stores, and running payment-enabled agent workflows through the 1ly MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable real crypto payments, withdrawals, token launches, and trades. <br>
Mitigation: Use a dedicated low-balance wallet, set explicit small budgets or disable auto-spend, and require manual approval for withdrawals, key revocation, deletions, token launches, and trades. <br>
Risk: Wallet keys and seller API keys may be required for paid or seller actions. <br>
Mitigation: Prefer wallet-provider options over inline private keys, store secrets securely, and verify the npm package before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1lystore/1ly-payments) <br>
- [1ly homepage](https://1ly.store) <br>
- [1ly documentation](https://docs.1ly.store/) <br>
- [1ly MCP server npm package](https://www.npmjs.com/package/@1ly/mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, environment variables, and JSON tool input examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance covers wallet setup, spending budgets, MCP tool selection, seller workflows, and token workflow constraints.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
