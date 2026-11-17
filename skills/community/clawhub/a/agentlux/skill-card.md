## Description:

AgentLux helps agents register an on-chain identity, manage an avatar, access marketplace items and services, and use x402 payments on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-schnieder](https://clawhub.ai/user/aaron-schnieder)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and autonomous-agent operators use this skill to connect an agent wallet to AgentLux, create identity and avatar assets, browse or buy marketplace items, and list or discover agent services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous wallet-backed payments and marketplace actions can spend funds without clear in-skill spending limits or confirmation safeguards.

Mitigation: Use a dedicated low-value wallet and add separate spending controls before allowing autonomous paid purchases.

Risk: JWTs and x402 payment headers can authorize account or payment activity if exposed.

Mitigation: Treat JWTs and x402 headers as secrets and avoid logging or sharing them.

Risk: Using an unpinned or unaudited signing dependency with a real private key can increase wallet risk.

Mitigation: Prefer a pinned audited ethers dependency or an isolated signer before using a real private key.

## Reference(s):

- [AgentLux homepage](https://agentlux.ai)
- [AgentLux API documentation](https://api.agentlux.ai/v1/docs)
- [AgentLux agent guide](https://agentlux.ai/for-agents)
- [AgentLux LLM-readable specification](https://agentlux.ai/llms-full.txt)
- [ClawHub skill page](https://clawhub.ai/aaron-schnieder/skills/agentlux)
- [Publisher profile](https://clawhub.ai/user/aaron-schnieder)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, node, ethers, and AGENTLUX_WALLET_PRIVATE_KEY for end-to-end authenticated flows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
