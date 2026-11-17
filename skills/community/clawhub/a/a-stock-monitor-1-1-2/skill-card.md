## Description:

A Stock Monitor analyzes China A-share market data with market sentiment scoring, short- and long-term stock selection, real-time price monitoring, rankings, a Flask web interface, cron automation, and historical caching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuchl2002](https://clawhub.ai/user/xuchl2002)

### License/Terms of Use:

MIT

## Use Case:

External developers and traders can use this skill to set up an A-share stock monitoring and analysis workflow that combines market sentiment, technical indicators, watchlists, stock-selection scripts, and a local dashboard. Its market recommendations should be reviewed independently before any trading decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled web app is unsafe to expose as-is because the security evidence reports public admin credentials, a fixed session secret, and debug mode on all network interfaces.

Mitigation: Before any network exposure, replace default accounts, load a unique SECRET_KEY from the environment, disable debug mode, bind to localhost or deploy behind real authentication, and verify user persistence.

Risk: Automated jobs and local database paths can affect local files and scheduled behavior.

Mitigation: Review cron commands, working directories, and SQLite paths before enabling automation.

Risk: Stock recommendations can be incorrect, stale, or unsuitable for a user's financial situation.

Mitigation: Treat recommendations as informational analysis and validate them independently before making trading decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xuchl2002/skills/a-stock-monitor-1-1-2)
- [Author Blog](https://www.cnblogs.com/Jame-mei)
- [API Documentation](artifact/references/API.md)
- [Installation Guide](artifact/references/INSTALL.md)
- [Stock Selection Documentation](artifact/references/STOCK_SELECTION.md)
- [Data Source Configuration](artifact/references/DATA_SOURCE_FINAL.md)
- [Sina Finance Performance Test Report](artifact/references/SINA_TEST_REPORT.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python configuration snippets, and JSON API examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to run local Python scripts, start a Flask dashboard, configure OpenClaw cron jobs, and interpret outputs from live market-data sources and a local SQLite cache.]

## Skill Version(s):

1.1.2 (source: artifact/_meta.json and changelog, released 2026-02-24; ClawHub release version 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
