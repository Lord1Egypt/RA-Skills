## Description:

Provides instant $1-$5 USDC microloans on Base mainnet for AI agents, with fast disbursement, credit checks, and flexible repayment options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jbpin](https://clawhub.ai/user/jbpin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use AgentCredit to let autonomous agents check credit, request small USDC loans, repay loans, and use an x402 facilitator when a wallet has a temporary liquidity shortfall.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using this skill can create real USDC debt for an enabled agent.

Mitigation: Install only when the agent should access small real-money USDC credit, use a dedicated low-balance wallet, and monitor outstanding loans.

Risk: Misconfigured facilitator or pool details could route an agent to an unintended payment service.

Mitigation: Verify the facilitator URL and pool address before use, and set approval or spending limits where possible.

Risk: Fees increase over time for unpaid loans.

Mitigation: Repay promptly and monitor loan status so overdue balances do not accumulate or block further facilitator settlements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jbpin/skills/agentcredit)
- [AgentCredit API](https://agentlending.spekn.com)
- [Full AgentCredit Docs](https://agentlending.spekn.com/llms-full.txt)
- [x402 Discovery](https://agentlending.spekn.com/.well-known/x402.json)
- [A2A Agent Card](https://agentlending.spekn.com/.well-known/agent-card.json)
- [MCP Endpoint](https://agentlending.spekn.com/mcp)
- [Pool Wallet on BaseScan](https://basescan.org/address/0x510a64F194CB6196d34C93717d88f13aCF0C979f)
- [USDC Contract on BaseScan](https://basescan.org/address/0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913)
- [Operator](https://spekn.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with TypeScript, JSON, and HTTP examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes endpoint, wallet-signing, loan-limit, fee, and repayment guidance for using the AgentCredit service.]

## Skill Version(s):

0.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
