## Description:

Calculates multi-timeframe Binance Event Contract signals for BTCUSDT and ETHUSDT with entries, targets, stop loss, confidence, and position sizing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acwxpunh](https://clawhub.ai/user/acwxpunh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and traders use this skill to have an agent calculate structured Binance Event Contract trading signals for BTCUSDT and ETHUSDT from K-line, liquidity, ICT structure, and risk inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce highly confident trading suggestions and position sizes that users could mistake for reliable investment advice.

Mitigation: Treat outputs as informational signals only, review assumptions and market data independently, and do not rely on stated win rates or sizing as financial advice.

Risk: The installation command references a mutable latest package version.

Mitigation: Prefer a pinned, reviewed installer version before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/acwxpunh/skills/binance-event-contract-signal)
- [Publisher profile](https://clawhub.ai/user/acwxpunh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style trading signal text with prices, targets, stop loss, confidence, confluence factors, and risk notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return Signal Pending when required market, liquidity, or structure data is missing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
