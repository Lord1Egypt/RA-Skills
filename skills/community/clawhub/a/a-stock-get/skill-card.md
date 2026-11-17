## Description:

Specialized A-share stock data collector. Automatically fetch and store daily/weekly/monthly historical K-line data for all A-share stocks in SQLite database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiyunnet](https://clawhub.ai/user/xiyunnet)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, data engineers, and quantitative analysts use this skill to collect Chinese A-share stock lists and daily, weekly, and monthly K-line data into a local SQLite database for market data analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts write to and mutate a fixed local D:\xistock storage location, including SQLite database records and market data files.

Mitigation: Run in an isolated virtual environment, confirm the storage path before use, and back up the database before reset or repair actions.

Risk: The artifact includes dependency guidance that names sqlite3 for pip installation and does not pin external package versions.

Mitigation: Do not run pip install sqlite3; use Python's standard-library sqlite3 module and prefer pinned versions for requests, pandas, and akshare.

Risk: Repair and reset workflows can delete or rewrite local data, and scheduling can add cron jobs or Telegram announcements.

Mitigation: Review repair prompts, reset commands, cron configuration, and notification settings before enabling automated jobs.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/xiyunnet/skills/a-stock-get)
- [AkShare Documentation](https://akshare.readthedocs.io/)
- [Python sqlite3 Documentation](https://docs.python.org/3/library/sqlite3.html)
- [Tencent Finance K-line Endpoint](https://proxy.finance.qq.com/ifzqgtimg/appstock/app/newfqkline/get)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python script references, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents through local SQLite setup, A-share data fetch commands, validation, repair, and optional scheduling workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
