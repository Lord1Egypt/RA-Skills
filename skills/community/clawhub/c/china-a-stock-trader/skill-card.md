## Description:

Provides Chinese A-share market analysis, stock screening, technical indicators, risk checks, market sentiment, Dragon-Tiger list data, and buy/hold/sell-style informational outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxie48892-jpg](https://clawhub.ai/user/dxie48892-jpg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze China A-share stocks, screen candidates, review market heat and Dragon-Tiger list signals, and receive risk-aware informational trading analysis. The outputs should support research and review, not replace independent financial judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock advice can be incorrect or stale because it depends on external market-data sources.

Mitigation: Treat buy, hold, and sell outputs as informational and verify data freshness and source quality before acting.

Risk: The skill can fall back to example records when live data or dependencies fail.

Mitigation: Do not trade from fallback or mock records; confirm that live data retrieval succeeded.

Risk: Unpinned or unreviewed dependencies can change behavior.

Mitigation: Install dependencies from a pinned, reviewed environment.

## Reference(s):

- [A-share stock code reference](references/china-stocks.md)
- [ClawHub skill page](https://clawhub.ai/dxie48892-jpg/skills/china-a-stock-trader)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown and text analysis with Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on outbound market-data queries and can fall back to example data when live data fails.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
