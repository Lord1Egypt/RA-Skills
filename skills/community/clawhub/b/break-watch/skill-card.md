## Description:

Break Watch scans live A-share market data for stocks that combine elevated volume, price gains, and bullish intraday candles, then returns structured trading signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hunkguo](https://clawhub.ai/user/hunkguo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use Break Watch to run explicit intraday A-share scans and summarize stocks matching breakout-volume, price-rise, and bullish-candle criteria for monitoring or review. Results are informational and not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned Python dependencies may resolve different package versions over time.

Mitigation: Install in an isolated Python environment, pin or approve dependencies before deployment, and avoid installing pyinstaller unless packaging is needed.

Risk: Generated .sel or CSV-like exports may contain unsanitized remote market-data fields.

Mitigation: Treat exported files as untrusted, sanitize stock-name fields before spreadsheet use, and prefer JSON or HTML review when sanitization is not available.

Risk: Scanner results may be stale outside trading hours or mistaken for investment advice.

Mitigation: Invoke the scanner only for explicit scan requests, surface trading-hours status, and present results as monitoring or review information only.

## Reference(s):

- [Break Watch strategy reference](references/strategy.md)
- [Break Watch ClawHub skill page](https://clawhub.ai/hunkguo/skills/break-watch)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [JSON scanner output with Markdown summaries and optional CSV-like, HTML, and text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live pytdx market data; optional file outputs are written under the configured result directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
