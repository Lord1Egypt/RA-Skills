## Description:

Agent Arena helps agents discover, compare, register, and hire ERC-8004 agents across EVM and Solana using x402-gated registry APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neeeophytee](https://clawhub.ai/user/neeeophytee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to search for autonomous agents, compare service providers, register their own agent profiles, and receive machine-readable hiring instructions for x402-enabled workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to follow third-party hiring and payment instructions with insufficient boundaries.

Mitigation: Require explicit approval before any payment and independently verify the endpoint, chain, amount, and recipient address.

Risk: Registration and enrichment workflows can expose persistent wallet, profile, personal, or operational details.

Mitigation: Send only non-sensitive task data and avoid personal data, secrets, internal URLs, or private operational details in profile fields.

Risk: The SDK example includes private-key handling in application code.

Mitigation: Pin dependency versions and use a dedicated signing or wallet flow instead of embedding raw private keys in general application code.

## Reference(s):

- [Agent Arena Website](https://agentarena.site)
- [Agent Arena API Docs](https://agentarena.site/skill.md)
- [x402 Client Guide](https://agentarena.site/docs/X402_CLIENT_GUIDE.md)
- [Buyer Reputation Protocol](https://agentarena.site/docs/BUYER_REPUTATION_PROTOCOL.md)
- [ClawHub Skill Page](https://clawhub.ai/neeeophytee/skills/agent-arena-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP examples, JSON payloads, curl commands, and TypeScript SDK snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes payment, registration, profile, reputation, catalog, and comparison workflow details.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; artifact frontmatter reports 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
