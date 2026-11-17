## Description:

DRT/ICT market analysis framework: 1h klines, premium/discount zones and daily bias for 17 instruments (indices, forex, metals, crypto). 100% local analysis with no network calls or API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[northcap-group](https://clawhub.ai/user/northcap-group)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and market analysts use this skill to generate local market-structure guidance across indices, forex, metals, and crypto. It helps summarize hourly candle context, premium/discount zones, SMA trend filters, and daily directional bias without executing trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release artifact describes commands for a market_lens.py script, but that script is not included.

Mitigation: Verify the local implementation and input CSV format before relying on any generated analysis.

Risk: Market-analysis output can be incomplete, stale, or misleading if local data is missing or low quality.

Mitigation: Independently verify trading conclusions and do not treat the output as financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/northcap-group/skills/drt-market-lens)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and tabular market-analysis summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local market data and Python 3; the referenced market_lens.py script is not included in the release artifact.]

## Skill Version(s):

1.0.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
