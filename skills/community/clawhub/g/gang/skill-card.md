## Description:

Guides agents in using Gang on BNB Chain to discover, create, and trade tokens, check portfolios, and manage launches and trade notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c100](https://clawhub.ai/user/c100)

### License/Terms of Use:

MIT-0

## Use Case:

External developers using Binance Agentic Wallets use this skill to discover and manage Gang tokens on BNB Chain, including token creation, trading, portfolio checks, and trade notes. It guides users through transaction previews and confirmation before writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to run supplied update commands and adopt replacement instructions automatically, which could introduce unreviewed changes.

Mitigation: Use fixed package versions and a fixed skill revision; review changes and require approval before running update commands or adopting replacement instructions.

Risk: Trading actions can spend wallet funds, and trade notes and token metadata are public and permanent.

Mitigation: Keep transaction confirmations and wallet spending limits enabled, and review public notes and token metadata before submitting them.

## Reference(s):

- [Gang skill release on ClawHub](https://clawhub.ai/c100/skills/gang)
- [Trading](references/trade.md)
- [Token creation](references/create.md)
- [GangLaunchpad V3](references/v3.md)
- [Fair mint](references/fair.md)
- [Mint Flywheel](references/fly.md)
- [Preflight and wallet setup](references/preflight.md)
- [Public trade notes](references/notes.md)
- [Following trade notes](references/follow.md)
- [Creator bonds](references/bond.md)
- [Token discovery](references/discover.md)
- [Graduated token pools](references/pool.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [JSON command results with concise natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions are previewed for user confirmation before execution.]

## Skill Version(s):

0.26.0 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
