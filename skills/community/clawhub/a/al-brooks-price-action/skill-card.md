## Description:

Analyze charts, OHLC bars, candlestick sequences, and trading context using Al Brooks style price action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ovels](https://clawhub.ai/user/ovels)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading analysts use this skill to interpret OHLC data, chart screenshots, and multi-timeframe summaries through a Brooks-style price action lens. It classifies market context, identifies the active setup near the hard right edge, and frames outcomes as actionable, watch, or no trade.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce entry, stop, and target ideas for trading prompts.

Mitigation: Treat outputs as chart analysis to review, not instructions to trade.

Risk: The skill may be invoked automatically on relevant trading prompts.

Mitigation: Install it only when Brooks-style trading chart interpretation is an intended agent capability.

## Reference(s):

- [Core Concepts](references/core_concepts.md)
- [Market Context Checklist](references/market_context_checklist.md)
- [Setup Taxonomy](references/setup_taxonomy.md)
- [Entries And Exits](references/entries_and_exits.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Guidance]

**Output Format:** [Markdown with optional JSON block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces market context, setup classification, tradeability status, entry, stop, target, trade style, invalidation, and a plain-language bottom line.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
