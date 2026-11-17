## Description:

Creates SVG candlestick charts and price-movement summaries for tokens on supported EVM chains and Solana using Chord trade data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuantqse90](https://clawhub.ai/user/tuantqse90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can chart token price history across supported chains and summarize changes, price ranges, volume, and trades from Chord data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unescaped token symbols from external data may alter generated SVG content.

Mitigation: Do not open generated charts for loosely resolved symbols in script-capable browsers until SVG text is escaped.

Risk: Chart requests send token information to Chord's API.

Mitigation: Use the skill only when sharing those token requests with Chord is acceptable.

Risk: Similar token symbols can resolve to an unintended asset.

Mitigation: Check the resolved token address before relying on a chart or its summary.

## Reference(s):

- [Chord](https://getchord.xyz)
- [Chord Charts on ClawHub](https://clawhub.ai/tuantqse90/skills/chord-charts)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [SVG candlestick chart and plain-language summary; JSON summary from the chart script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the resolved token address, price change, high, low, volume, trades, and whether the last candle is open.]

## Skill Version(s):

1.1.2 (source: server-resolved ClawHub release; artifact metadata says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
