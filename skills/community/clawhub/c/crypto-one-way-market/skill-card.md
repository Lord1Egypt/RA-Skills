## Description:

Fetch cryptocurrency OHLCV candle data and judge whether the market is in a one-way bullish or bearish trend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoxin06666](https://clawhub.ai/user/xiaoxin06666)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to fetch public crypto candle data and summarize whether a selected symbol and timeframe shows a bullish one-way trend, bearish one-way trend, weak trend, or range/chop structure. The output is market-structure analysis and not trading advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public Binance-compatible API requests can fail, be blocked by region, or return unavailable data.

Mitigation: Confirm that the target endpoint is accessible before relying on a result, and use the configurable base URL only when the user provides or approves an accessible compatible endpoint.

Risk: Candle-only market-structure analysis can become stale during sudden crypto regime shifts or news events.

Mitigation: Present confidence and invalidation conditions, avoid certainty, and make clear that the result describes only the sampled interval.

Risk: Optional CSV export writes candle data to a local path selected at runtime.

Mitigation: Use explicit output paths and review generated CSV files before sharing or reusing them.

Risk: Users may mistake trend classification for live trading advice.

Mitigation: Frame outputs as market-structure analysis, not trade instructions, and mention liquidity, news, and contract-basis limitations for live trading contexts.

## Reference(s):

- [Methodology](references/methodology.md)
- [ClawHub skill page](https://clawhub.ai/xiaoxin06666/skills/crypto-one-way-market)
- [Binance US API endpoint](https://api.binance.us)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV files, Shell commands, Guidance]

**Output Format:** [Markdown summary with optional JSON payload and optional CSV candle export.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes symbol, exchange source, interval, candle count, time span, classification, confidence, directional return, trend efficiency, ADX, ATR-normalized move, max pullback, moving-average agreement, and invalidation notes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
