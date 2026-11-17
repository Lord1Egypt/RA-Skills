## Description:

Private DeFi for AI agents: shield tokens into a Railgun ZK privacy pool, swap privately, lend into Morpho vaults for yield, and bridge cross-chain via LI.FI on Base, Arbitrum, and BSC.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mmchougule](https://clawhub.ai/user/mmchougule)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate DeFi workflows through an agent, including private shielding, swaps, lending, redemption, cross-chain transfer, and strategy execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs mutable third-party install code.

Mitigation: Install only a reviewed, pinned package version before use.

Risk: The skill can move funds through wallet-authorized DeFi actions.

Mitigation: Keep wallet funds limited and manually review every route, amount, destination, and chain before signing.

Risk: Private key and wallet file exposure could compromise funds.

Mitigation: Protect or isolate WORKER_PRIVATE_KEY and ~/.b402/wallet.json.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mmchougule/skills/b402-private-defi)
- [b402 SDK homepage](https://github.com/b402-ai/b402-sdk)
- [b402 MCP package](https://npmjs.com/package/b402-mcp)
- [b402 SDK package](https://npmjs.com/package/@b402ai/sdk)
- [b402 starter](https://github.com/b402-ai/b402-starter)
- [b402 agent starter](https://github.com/b402-ai/b402-agent-starter)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, npx, and WORKER_PRIVATE_KEY; installation configures a local wallet and MCP server.]

## Skill Version(s):

0.4.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
