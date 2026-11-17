## Description:

实时竞品监控虾 helps agents track competitor prices, ratings, review counts, promotions, and price-change events, using the bundled local workflow and analysis references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business analysts use this skill to maintain competitor watchlists, run local price checks, inspect price-change events, and generate periodic competitor reports. Developers can adapt the simulated collector into a production data collector after legal, platform-access, and notification-scope review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Monitoring output may be mistaken for live marketplace intelligence while the bundled collector uses simulated data.

Mitigation: Treat generated prices, ratings, and review counts as demonstration data until the collector is replaced with a reviewed production data source.

Risk: Future real scraping, cookie, proxy, or platform-access setup may create legal, terms-of-service, or account-risk exposure.

Mitigation: Review platform permissions, rate limits, credential handling, and collection scope before enabling real scraping.

Risk: Price alerts sent to Feishu or other messaging channels may reach unintended recipients or expose competitor-monitoring strategy.

Mitigation: Limit notification recipients, review message contents, and confirm channel authorization before forwarding alerts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tujinsama/skills/competitor-monitor-claw)
- [Competitor analysis framework](references/competitor-analysis-framework.md)
- [Industry benchmarks](references/industry-benchmarks.md)
- [Platform scraping rules](references/platform-scraping-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, CSV configuration, SQLite-backed local reports, and terminal output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses simulated collection data by default; local history is stored in SQLite under data/competitor_monitor.db.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
