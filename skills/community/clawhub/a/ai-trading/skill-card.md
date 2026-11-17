## Description:

Research US stocks and ETFs like a buy-side analyst: live quotes, technicals, fundamentals, sector context, backtests and a written trade plan with position sizing and hard risk rules. Human approval is required before any order - analysis and education, never financial advice or auto-trading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

Investors and analysts use this skill to research US stocks and ETFs, review market data and fundamentals, and prepare written research and risk-based trade plans. It supports human-reviewed analysis and does not place orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verified calculation errors may affect figures and position sizes; some stated risk rules are not enforced.

Mitigation: Independently verify volume, historical ranges, position sizes, and risk-rule checks against trusted data and calculations before relying on research output.

Risk: The overnight flag does not halve share counts, and live API support needs repair.

Mitigation: Do not rely on the overnight adjustment or unrepaired live API workflows; independently check calculations and use market-data keys only.

## Reference(s):

- [AI Trading release](https://clawhub.ai/rapidworker1/skills/ai-trading)
- [Data sources](references/data-sources.md)
- [Risk playbook](references/risk-playbook.md)
- [US market calendar](references/us-market-calendar.md)
- [SEC EDGAR company facts API](https://data.sec.gov/api/xbrl/companyconcept/CIK0000320193/us-gaap/Revenues.json)
- [NYSE hours and calendars](https://www.nyse.com/markets/hours-calendars)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Guidance]

**Output Format:** [Markdown research reports and trade plans, with JSON market snapshots and position-sizing plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Based on user-provided ticker, time horizon, thesis, market data, and risk rules; outputs require independent review and explicit human approval before any action.]

## Skill Version(s):

1.0.5 (source: release metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
