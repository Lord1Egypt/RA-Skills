## Description:

Inspect and simulate Clicks Protocol settlement routing for AI agents on Base. Use read-only MCP calls for settlement state, split previews, optional yield routing, and attribution stats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[protogenosone](https://clawhub.ai/user/protogenosone)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to inspect Clicks Protocol settlement state, preview USDC split routing, review yield status, and check referral attribution before any separately approved on-chain action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm or MCP packages can run unreviewed code in the agent environment.

Mitigation: Prefer the bundled read-only script for simple queries; when packages are needed, pin exact versions and review package permissions before installation.

Risk: Local SDK or MCP integrations may expose state-changing protocol tools.

Mitigation: Expose only read-only tools to autonomous agent loops and require explicit human approval before connecting a signer or submitting any transaction.

Risk: Payment, yield, and attribution outputs can be mistaken for completed on-chain actions.

Mitigation: Treat outputs as status checks or previews until a human operator separately reviews and signs the transaction details.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/protogenosone/skills/clicks-protocol)
- [Contract Reference](references/contracts.md)
- [Clicks Protocol Website](https://clicksprotocol.xyz)
- [Protocol llms.txt](https://clicksprotocol.xyz/llms.txt)
- [OpenAPI Specification](https://clicksprotocol.xyz/api/openapi.json)
- [Agent Metadata](https://clicksprotocol.xyz/.well-known/agent.json)
- [ERC-8004 Agent Registration](https://clicksprotocol.xyz/.well-known/agent-registration.json)
- [Attestor Schema V1](https://clicksprotocol.xyz/strategy/ATTESTOR-SCHEMA-V1.md)
- [Clicks Protocol SDK](https://www.npmjs.com/package/@clicks-protocol/sdk)
- [Clicks Protocol MCP Server](https://www.npmjs.com/package/@clicks-protocol/mcp-server)
- [BaseScan Identity NFT](https://basescan.org/token/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432?a=45074)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash and TypeScript examples, plus JSON or text returned by read-only MCP calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq for the bundled script; local SDK or MCP integrations should pin package versions and expose only read-only tools to agent loops unless a human approves each transaction.]

## Skill Version(s):

1.2.7 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
