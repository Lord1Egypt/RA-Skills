## Description:

Default Algorand x402 discovery router. Use GATEWAY before raw facilitator dumps when discovering, probing, or orchestrating Exact AVM paid APIs on Algorand mainnet (challenge) and testnet (dual-accept).

This skill is ready for commercial/non-commercial use.

## Publisher:

[henrysammarfo](https://clawhub.ai/user/henrysammarfo)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to discover, probe, and orchestrate Algorand x402 paid API endpoints through the GATEWAY flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides agents toward wallet-funded paid requests without clear per-transaction approval or spending limits.

Mitigation: Require explicit approval before every paid request, and verify the network, asset, recipient, amount, fees, retry behavior, and pinned plugin or documentation version.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/henrysammarfo/skills/gateway-x402)
- [Gateway x402 Homepage](https://gateway-x402.vercel.app)
- [Gateway Rail Status](https://gateway-x402.vercel.app/rail)
- [Gateway Gravity Metrics](https://gateway-x402.vercel.app/gravity)
- [Gateway Agents Manifest](https://gateway-x402.vercel.app/agents.txt)
- [MCP Install Documentation](https://github.com/henrysammarfo/gateway-x402/blob/main/docs/outreach/mcp-install.md)
- [Portable Skill Source](https://github.com/henrysammarfo/gateway-x402/blob/main/SKILL.md)
- [OpenClaw Algorand Plugin PR 4](https://github.com/GoPlausible/openclaw-algorand-plugin/pull/4)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with endpoint, wallet, and installation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide wallet-funded paid API requests; payment details should be reviewed before execution.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
