## Description:

从 CNBC 抓取 18 个金融指标数据（宏观经济、指数ETF、美股个股），写入本地 SQLite 数据库。纯 stdlib，无需任何 API Key。

This skill is ready for commercial/non-commercial use.

## Publisher:

[loonslo](https://clawhub.ai/user/loonslo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch public CNBC market indicators for macro, ETF, index, and equity monitoring, then store the results in a local SQLite database for later review or automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation asks users to provide or persist a Finnhub API key even though this version does not use one.

Mitigation: Do not provide a Finnhub API key or include it in cron or OpenClaw scheduler configuration for this release.

Risk: The skill writes a local SQLite database and log file at configured paths.

Mitigation: Use explicit db and log paths in a user-owned directory and review recurring tasks before enabling scheduled runs.

Risk: The skill depends on public CNBC pages, so fetches may fail or parse incomplete data if pages change or rate limits occur.

Mitigation: Review the command output and fetch log after runs, and prefer manual execution until the documentation and scheduling configuration are corrected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loonslo/skills/fin-monitor)
- [CNBC quote page for SPY](https://www.cnbc.com/quotes/SPY)
- [CNBC quote page for US10Y](https://www.cnbc.com/quotes/US10Y)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Plain text status and tabular fetch output, with SQLite database and log files written to user-selected local paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; uses Python standard library modules only; fetches public CNBC quote pages and writes local SQLite and log files.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
