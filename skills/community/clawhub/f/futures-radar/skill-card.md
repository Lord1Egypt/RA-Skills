## Description:

Futures Radar helps agents fetch and summarize live futures and commodity market data from Yahoo Finance for energy, metals, agricultural contracts, Treasury futures, and DXY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gold3bear](https://clawhub.ai/user/gold3bear)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to monitor commodity and futures markets, retrieve current Yahoo Finance quotes, and frame high-level signals such as gold-silver and oil-gold ratios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes live network requests to Yahoo Finance for market data.

Mitigation: Use it only in environments where outbound requests for public market data are allowed and expected.

Risk: Market data may be delayed, unavailable, or unsuitable as the sole basis for financial decisions.

Mitigation: Treat outputs as informational market context and verify important quotes with an authoritative source before acting.

Risk: The artifact is written for Chinese-language output and broad commodity or futures activation terms.

Mitigation: Deploy where Chinese-language market summaries are appropriate, and review activation behavior if narrower routing is required.

## Reference(s):

- [Futures Radar ClawHub listing](https://clawhub.ai/gold3bear/skills/futures-radar)
- [Publisher profile: gold3bear](https://clawhub.ai/user/gold3bear)
- [Yahoo Finance chart API endpoint used by the skill](https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Chinese-language terminal text and Markdown guidance with optional Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live market data depends on Yahoo Finance availability and network access.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
