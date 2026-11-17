## Description:

Provides A-share K-line and intraday price data lookup for individual stocks, including daily, weekly, monthly, and yearly OHLC data, volume, turnover, MA5/MA10/MA20 moving averages, and one-minute intraday prices from market.ft.tech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawn92](https://clawhub.ai/user/shawn92)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve recent and historical A-share OHLC and one-minute intraday market data for a single stock. It is suited for answering stock chart, open-high-low-close, volume, turnover, moving-average, and intraday trend questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local Python router can be tricked into running an unintended handler path if invoked with an unsafe sub-skill name.

Mitigation: Patch or wrap the router so it only accepts the two bundled sub-skill names, stock-ohlcs and stock-prices, before using it where prompts or users can influence command arguments.

Risk: The skill retrieves live market data from market.ft.tech and depends on that service for freshness and availability.

Mitigation: Tell users when data may be delayed or unavailable and avoid presenting retrieved values as investment advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shawn92/skills/ftshare-kline-data)
- [market.ft.tech API base](https://market.ft.tech/app)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [JSON data summarized as concise Markdown tables or bullet points]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns stock-specific market data, with ISO-formatted Beijing-time timestamps produced by the bundled handlers.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
