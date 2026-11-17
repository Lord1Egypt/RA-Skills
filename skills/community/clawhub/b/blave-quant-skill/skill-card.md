## Description:

Blave quant data layer and exchange-trading reference for AI agents, covering crypto and Taiwan market data, futures data, Hyperliquid trader information, and trading across supported exchanges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blave-wei](https://clawhub.ai/user/blave-wei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative traders use the skill to retrieve crypto, Taiwan stock, and futures data, consult exchange API guidance, and carry out exchange trading workflows. It requires explicit current-conversation confirmation for each order, cancellation, transfer, or funding action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks this release suspicious, citing marketplace strategy-download and execution workflows, BitMart transfers, and affiliate-data access beyond the stated market-data and trading purpose; scanner coverage is incomplete.

Mitigation: Review downloaded strategy content before execution, limit API-key permissions to the actions needed, and require the skill’s explicit current-conversation confirmation separately for each write action.

## Reference(s):

- [Blave Documentation](https://blave.org/docs/en)
- [Blave API Setup](https://blave.org/landing/en/api?tab=blave)
- [ClawHub Release Page](https://clawhub.ai/blave-wei/skills/blave-quant-skill)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Analysis, Configuration instructions]

**Output Format:** [Markdown guidance, API requests, and market or account data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only market and account queries; write actions require explicit confirmation for each action.]

## Skill Version(s):

1.25.8 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
