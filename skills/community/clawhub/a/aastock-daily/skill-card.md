## Description:

Aastock Daily generates scheduled A-share market briefs and portfolio-tracking reports using Eastmoney market and news data, including pre-market, close, night, weekend, announcements, research headlines, and community sentiment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[torchesfrms](https://clawhub.ai/user/torchesfrms)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure and run A-share market briefing scripts for daily market summaries and portfolio monitoring. It is intended for informational reporting workflows around configured holdings, schedules, announcements, research headlines, and community sentiment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling is unclear and the release may use embedded or silently loaded API credentials.

Mitigation: Install only after the publisher removes embedded keys and documents required credentials and network access; test with disposable credentials first.

Risk: Financial reports may contain simulated, stale, or unsourced values that could mislead users.

Mitigation: Treat output as informational until API responses and timestamps are validated; compare market-sensitive values against trusted data before acting.

Risk: Portfolio configuration can reveal sensitive holdings.

Mitigation: Test in a sandbox with non-sensitive holdings and avoid storing real portfolios until the publisher addresses the security guidance.

## Reference(s):

- [Aastock Daily ClawHub listing](https://clawhub.ai/torchesfrms/skills/aastock-daily)
- [Eastmoney authenticated API host](https://mkapi2.dfcfs.com)
- [Eastmoney quote API host](http://push2.eastmoney.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese text reports with Markdown-like sections and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured holdings and network access to Eastmoney data sources.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter and changelog report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
