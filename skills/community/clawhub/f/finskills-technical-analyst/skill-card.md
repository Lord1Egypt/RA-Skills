## Description:

Perform comprehensive technical analysis using 12+ indicators including RSI, MACD, Bollinger Bands, support/resistance, and chart patterns via the Finskills API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finskills](https://clawhub.ai/user/finskills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to request technical analysis for US-listed stocks, ETFs, and indexes. It retrieves Finskills market data, computes common indicators, maps support and resistance, and summarizes a trade setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README install command uses a mutable remote source.

Mitigation: Install only after reviewing the exact source and prefer a pinned commit or verified release.

Risk: The skill can produce actionable entry, stop-loss, target, and recommendation fields.

Mitigation: Treat outputs as informational technical analysis, not financial advice, and require user judgment before trading.

Risk: The skill requires a Finskills API key.

Mitigation: Provide only an API key approved for this third-party service and avoid exposing credentials in prompts, logs, or shared transcripts.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/finskills/skills/finskills-technical-analyst)
- [Finskills Technical Analyst repository](https://github.com/finskills/technical-analyst)
- [Finskills API](https://finskills.net)
- [Finskills API registration](https://finskills.net/register)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown-style technical analysis with indicator tables, support/resistance levels, and trade setup fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FINSKILLS_API_KEY and access to Finskills historical OHLCV endpoints.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.2 and README badge lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
