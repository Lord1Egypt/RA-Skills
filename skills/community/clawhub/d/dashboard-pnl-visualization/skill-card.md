## Description:

Trading dashboard P&L visualization with profit tracker integration, win-rate overlays, R-multiples, and configurable settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sarkcesscrewpay](https://clawhub.ai/user/sarkcesscrewpay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-dashboard builders use this skill to add P&L breakdowns, win-rate overlays, R-multiple displays, and runtime configuration patterns to trading monitoring dashboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dashboard outputs and logs may expose financial account performance.

Mitigation: Review generated dashboards and logs before sharing or deploying them.

Risk: Trading API credentials could be mishandled when adapting the dashboard patterns.

Mitigation: Keep Alpaca credentials outside the skill and use read-only or least-privilege API access where possible.

Risk: R-multiple values can be misleading when stop prices are absent or invalid.

Mitigation: Return no R-multiple and display a neutral placeholder when stop-price data is missing or risk per share is non-positive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sarkcesscrewpay/skills/dashboard-pnl-visualization)
- [Publisher profile](https://clawhub.ai/user/sarkcesscrewpay)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with Python code examples and configuration parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces implementation patterns for dashboard configuration, broker equity history retrieval, profit-summary overlays, realized and unrealized P&L splits, and R-multiple visualization.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
