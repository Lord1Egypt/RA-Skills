## Description:

Process Avanza CSV exports, calculate TWRR/Modified Dietz returns, and track portfolio performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patello](https://clawhub.ai/user/patello)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to import Avanza transaction CSVs, maintain a local SQLite portfolio database, calculate investment performance, inspect holdings, and generate portfolio reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Declared file access is narrower than the code behavior, and portfolio databases or backup files may contain sensitive financial data.

Mitigation: Use a private data directory, review import and export paths before running commands, and protect or delete generated backup files when they are no longer needed.

Risk: Portfolio asset names may be sent to Avanza by default when live prices are updated, and benchmark/date information may be sent to Riksbanken or Yahoo Finance for risk metrics.

Mitigation: Use --update-prices never for offline operation and run --risk or --beta only when those external requests are acceptable.

Risk: Destructive commands can permanently remove transactions or account data.

Mitigation: Back up the database first, prefer dry-run previews where available, and avoid --yes unless the intended deletion scope has been reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/patello/skills/avanza-investment-tracker)
- [Workflows](references/workflows.md)
- [Troubleshooting](references/troubleshooting.md)
- [Avanza Public API](https://www.avanza.se)
- [Riksbanken API](https://api.riksbank.se)
- [Yahoo Finance Query API](https://query1.finance.yahoo.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented guidance with inline shell commands and optional JSON/table CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide commands that read and write a user-specified SQLite database and optionally call external market-data APIs.]

## Skill Version(s):

2.14.1 (source: ClawHub release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
