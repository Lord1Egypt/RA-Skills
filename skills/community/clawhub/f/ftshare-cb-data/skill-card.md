## Description:

Provides A-share convertible bond lists, single-bond fundamentals, historical candlestick data for convertible bonds and A-shares, and trading-date lookups using market.ft.tech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawn92](https://clawhub.ai/user/shawn92)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Chinese convertible-bond market-data questions, including listing bonds, retrieving fundamentals, fetching historical K-lines, and calculating recent trading-date windows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends bond symbols, date ranges, interval settings, and similar market-query parameters to market.ft.tech.

Mitigation: Install and run it only when that external data-service dependency and query disclosure are acceptable.

Risk: The documentation is Chinese-only, which can increase the chance of misunderstanding parameters or market-data limitations.

Mitigation: Have a Chinese-reading reviewer confirm intended usage and user-facing explanations before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shawn92/skills/ftshare-cb-data)
- [market.ft.tech data service](https://market.ft.tech)
- [Convertible bond list endpoint](https://market.ft.tech/data/api/v1/market/data/cb/cb-lists)
- [Convertible bond base-data endpoint](https://market.ft.tech/data/api/v1/market/data/cb/cb-base-data)
- [Stock candlesticks endpoint](https://market.ft.tech/data/api/v1/market/data/stock-candlesticks)
- [Nth trading-date endpoint](https://market.ft.tech/data/api/v1/market/data/time/get-nth-trade-date)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [JSON from Python scripts, typically summarized by the agent as Markdown tables or bullets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries disclosed market.ft.tech endpoints with bond symbols, date ranges, interval settings, and trading-date counts.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
