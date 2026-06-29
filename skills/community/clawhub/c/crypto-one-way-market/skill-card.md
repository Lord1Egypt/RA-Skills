## Description: <br>
Fetch cryptocurrency OHLCV candle data and judge whether the market is in a one-way bullish or bearish trend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoxin06666](https://clawhub.ai/user/xiaoxin06666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to fetch public cryptocurrency candles and classify whether the sampled market structure is a bullish one-way trend, bearish one-way trend, weak trend, or range/chop. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes public Binance-compatible market-data requests. <br>
Mitigation: Use it only where outbound requests to the selected exchange endpoint are acceptable, and review any custom --base-url before execution. <br>
Risk: The skill can write candle data to a CSV path when requested. <br>
Mitigation: Choose an intended output path and review generated files before sharing or reusing them. <br>
Risk: Trend classification can be mistaken for trading advice. <br>
Mitigation: Present results as sampled market-structure analysis, include uncertainty and invalidation notes, and avoid trade instructions. <br>


## Reference(s): <br>
- [Methodology](references/methodology.md) <br>
- [Binance US API endpoint](https://api.binance.us) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown summaries with optional JSON or CSV output from the bundled script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports symbol, exchange source, interval, candle count, time span, classification, confidence, directional metrics, and risk notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
