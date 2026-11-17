## Description:

Uses the Eastmoney API to retrieve intraday time-series market data for Shanghai and Shenzhen A-shares and major Chinese indexes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bensema](https://clawhub.ai/user/bensema)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market-data agents use this skill to look up same-day intraday price, volume, turnover, and average-price data for supported A-shares and indexes. The result is informational market data and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the requested stock or index identifier to Eastmoney.

Mitigation: Avoid using sensitive or confidential identifiers in requests, and review Eastmoney data-handling expectations before use.

Risk: Market data can be stale or unavailable, especially outside trading hours when the API may return the previous trading day.

Mitigation: Check the returned timestamp/date and verify important trading decisions with an authoritative financial source.

Risk: The returned market data may be mistaken for financial advice.

Mitigation: Present the output as informational data only and avoid recommending trades based solely on the skill response.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bensema/skills/dfcf-stock-intraday)
- [Eastmoney trends2 quote API](https://push2.eastmoney.com/api/qt/stock/trends2/get)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown text with shell commands and tabular market data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Formats intraday records with HH:MM timestamps, two-decimal average prices, and notes when non-trading-hour requests may return the previous trading day.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
