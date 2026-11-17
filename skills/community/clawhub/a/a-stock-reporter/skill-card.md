## Description:

A-Stock Reporter helps agents query A-share stock quotes, generate market briefs, retrieve historical daily reports, and prepare scheduled trading-session updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laojun509](https://clawhub.ai/user/laojun509)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to produce Chinese A-share market snapshots, individual stock reports, historical daily summaries, and scheduled trading updates for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated market stance can be mistaken for financial advice.

Mitigation: Treat reports as informational market summaries and confirm decisions with qualified financial review.

Risk: Third-party public market data can be delayed, unavailable, or inaccurate.

Mitigation: Confirm time-sensitive prices and index data against an authoritative market data source before acting.

Risk: Cron entries create scheduled network activity and recurring reports.

Mitigation: Add cron entries only intentionally, and review the schedule, environment paths, and report destination before enabling them.

Risk: Dependency versions are not pinned in the artifact documentation.

Mitigation: Install in a virtual environment and pin reviewed dependency versions before routine use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/laojun509/skills/a-stock-reporter)
- [Strategy Rules](references/rules.md)
- [Sector Definitions](references/sectors.json)
- [Watchlists](references/watchlist.json)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Chinese plain-text market reports with optional shell command snippets and cron entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on third-party public market data sources; historical reports may be read from saved files or fetched online.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
