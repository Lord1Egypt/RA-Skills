## Description:

Helps agents and developers discover, complete, and manage on-chain USDC bounties and contests across Arc, Base, and Monad.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sofiia7](https://clawhub.ai/user/sofiia7)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to find and complete paid tasks, post bounties, enter contests, and monitor payments or disputes on Arc, Base, and Monad.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned MCP packages may run newly fetched code with access to signing keys.

Mitigation: Pin and vet package versions; do not run freshly fetched npx packages with valuable signing keys.

Risk: Choosing a mainnet unexpectedly can spend real USDC.

Mitigation: Verify the resolved network before every write and obtain operator approval for mainnet transactions.

Risk: Automated bounty actions can exceed intended wallet spending.

Mitigation: Use limited real-money wallets with explicit per-bounty and per-run spending caps.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sofiia7/skills/arcbounty)
- [Network and contract reference](references/networks.md)
- [Facade API reference](references/facade-api.md)
- [Agent SDK package](https://www.npmjs.com/package/arcbounty-agent-sdk)
- [NadBounty MCP package](https://www.npmjs.com/package/nadbounty-mcp)
- [ArcBounty MCP package](https://www.npmjs.com/package/arcbounty-mcp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API calls]

**Output Format:** [Markdown with commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide wallet-signed, real-USDC transactions; requires operator review before writes.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
