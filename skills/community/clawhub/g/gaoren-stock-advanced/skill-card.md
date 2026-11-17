## Description:

Generates stock quote checks, technical indicators, news summaries, and multi-section analysis reports for HK, US, and A-share symbols using external market and news data sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaoren36-arch](https://clawhub.ai/user/gaoren36-arch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for stock quote checks and summarized technical or news analysis for HK, US, and A-share symbols. Outputs should be treated as informational summaries, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce buy, hold, sell, or stop-loss style guidance that may be mistaken for financial advice.

Mitigation: Label outputs as informational only and require qualified human review before any trading or portfolio decision.

Risk: At least one report path can calculate technical indicators from simulated random historical prices.

Mitigation: Require verified historical market data before presenting RSI, moving averages, MACD, scores, or recommendations as decision-support signals.

Risk: Artifact code includes a bundled Finnhub token in several scripts.

Mitigation: Remove or rotate bundled credentials and require users to provide their own API token through environment configuration.

Risk: The skill depends on external market and news services whose availability, freshness, and coverage may vary.

Mitigation: Show data-source context in reports and handle unavailable or incomplete data without substituting fabricated values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gaoren36-arch/skills/gaoren-stock-advanced)
- [Skill definition](artifact/SKILL.md)
- [Chinese README](artifact/README.md)
- [English README](artifact/README_EN.md)
- [Futu HK stock page example](https://www.futunn.com/stock/03998-HK)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or terminal-style text stock analysis reports with inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access for external market and news data; Python and curl are declared runtime dependencies.]

## Skill Version(s):

2.1.0 (source: server release metadata, OpenClaw metadata, and artifact version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
