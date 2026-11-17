## Description:

Gets recent A-share top-gainer rankings for a requested time window, filters out ST stocks, and returns a formatted stock table using iwencai market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shinelp100](https://clawhub.ai/user/shinelp100)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer questions about which A-share stocks gained the most over a recent N-day period. It produces a ranked, filtered table that excludes ST stocks and includes source, query time, and market-risk notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs browser JavaScript navigation to work around blocked navigation controls.

Mitigation: Use only in environments where this access pattern has been reviewed and approved; prefer a version that uses an approved market-data API or policy-compliant browser access.

Risk: The skill returns real-time or near-real-time market information that may be incomplete, delayed, or affected by source-page changes.

Mitigation: Treat outputs as informational, verify material decisions against authoritative market-data sources, and review failures when page structure changes.

Risk: Stock rankings and abnormal short-term gains can be mistaken for investment recommendations.

Mitigation: Keep the output framed as ranking data, preserve the risk note, and avoid presenting the table as financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shinelp100/skills/astock-top-gainers)
- [Publisher profile](https://clawhub.ai/user/shinelp100)
- [iwencai data source](https://www.iwencai.com)

## Skill Output:

**Output Type(s):** [text, markdown, analysis]

**Output Format:** [Markdown table with short explanatory text and risk note]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output includes requested lookback window, rank, stock code, name, price, daily change, interval rank, interval gain, data source, query time, and ST-stock filtering note.]

## Skill Version(s):

1.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
