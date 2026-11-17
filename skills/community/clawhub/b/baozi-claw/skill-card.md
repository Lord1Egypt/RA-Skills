## Description:

Complete Solana prediction markets skill for Baozi: list markets, get odds, place bets, and claim winnings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcusfranca12](https://clawhub.ai/user/marcusfranca12)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent browse Baozi prediction markets on Solana, inspect odds and positions, and prepare betting or claim actions. Any action involving funds should be reviewed and confirmed before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release advertises betting, claiming, portfolio, and market-creation behavior, but shipped implementation files include a placeholder example tool and a smaller runtime tool set.

Mitigation: Require the publisher to align the manifest, documentation, and implementation before installation or publication.

Risk: Betting-related tool instructions invoke runtime npx and shell execution.

Mitigation: Remove shell execution, pin and review dependencies, and call reviewed APIs directly.

Risk: Tools can build betting or claim transactions that may affect user funds.

Mitigation: Require explicit user confirmation and transaction review before any betting or claim action is submitted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marcusfranca12/skills/baozi-claw)
- [ClawHub publisher profile](https://clawhub.ai/user/marcusfranca12)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured tool results with inline code or shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce market data, portfolio summaries, transaction-building guidance, and installation commands; transaction-related outputs require user review.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
