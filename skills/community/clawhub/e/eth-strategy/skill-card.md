## Description:

Eth Strategy analyzes ETH/USDT and other trading pairs using technical indicators, candlestick patterns, volume zones, and simplified sentiment signals to produce directional trading levels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samary-xia](https://clawhub.ai/user/samary-xia)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate informational technical-analysis signals for cryptocurrency pairs, including direction, entry, stop-loss, and staged take-profit levels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated trading levels may be interpreted as financial advice and following them could cause financial loss.

Mitigation: Treat outputs as informational analysis only and require independent human review before any trading decision.

Risk: Runtime behavior depends on third-party Python packages and public market-data access.

Mitigation: Install in an isolated environment with pinned dependency versions where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samary-xia/skills/eth-strategy)

## Skill Output:

**Output Type(s):** [text, JSON, analysis]

**Output Format:** [JSON object printed as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prints an empty JSON object when no clear signal is generated.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
