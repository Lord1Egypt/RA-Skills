## Description: <br>
Integrate autonomous USDC yield into AI agent projects on Base by querying live APY, inspecting agent treasury state, simulating payment splits, using the MCP server, and implementing x402-aligned treasury flows with built-in three-level referrals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[protogenosone](https://clawhub.ai/user/protogenosone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add read-only Clicks Protocol treasury queries, payment-split simulations, and integration guidance for agents that hold or route USDC on Base. Teams can also use it to evaluate SDK and MCP-based flows for deposits, withdrawals, referrals, and yield settings before requiring human approval for any signed transaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-enabled SDK or local MCP operations can move real USDC. <br>
Mitigation: Use a dedicated low-balance wallet and require explicit human approval before any deposit, withdrawal, registration, yield-setting change, or other signed transaction. <br>
Risk: External npm packages and remote MCP endpoints affect financial workflows. <br>
Mitigation: Review and pin external packages, verify contract addresses against the contract reference, and limit unattended use to read-only queries. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/protogenosone/clicks-protocol) <br>
- [Clicks Protocol Website](https://clicksprotocol.xyz) <br>
- [Contract Reference](references/contracts.md) <br>
- [Clicks Protocol SDK](https://www.npmjs.com/package/@clicks-protocol/sdk) <br>
- [Clicks Protocol MCP Server](https://www.npmjs.com/package/@clicks-protocol/mcp-server) <br>
- [OpenAPI Specification](https://clicksprotocol.xyz/api/openapi.json) <br>
- [Agent Metadata](https://clicksprotocol.xyz/.well-known/agent.json) <br>
- [ERC-8004 Agent Registration](https://clicksprotocol.xyz/.well-known/agent-registration.json) <br>
- [LLMs Reference](https://clicksprotocol.xyz/llms.txt) <br>
- [Attestor Schema V1](https://clicksprotocol.xyz/strategy/ATTESTOR-SCHEMA-V1.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes read-only query commands that return MCP responses, plus SDK and MCP setup guidance for wallet-enabled flows.] <br>

## Skill Version(s): <br>
1.2.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
