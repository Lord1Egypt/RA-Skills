## Description:

Track the dividend premium (dividend yield minus 10-year bond yield) for CSI Dividend Low Volatility Index. Monitor dividend yield, 10-year bond yield, and calculate the premium for investment decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gykdly](https://clawhub.ai/user/gykdly)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to fetch Chinese dividend and bond yield data, calculate the CSI Dividend Low Volatility Index premium, generate CSV and Excel tracking reports, and check alert conditions for investment monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External alerting uses Telegram and includes a fixed chat ID in the artifact.

Mitigation: Do not configure TELEGRAM_BOT_TOKEN until the chat ID is user-configurable and the alert destination has been reviewed.

Risk: The artifact includes unsafe shell-based curl execution patterns.

Mitigation: Replace os.system curl calls with parameterized HTTP client calls before installation or scheduled use.

Risk: The scripts write CSV and Excel reports to a fixed local workspace path and may overwrite existing files.

Mitigation: Move outputs to a user-selected or skill-owned directory and review file overwrite behavior before running cron jobs.

Risk: The skill downloads Chinese market data during normal operation.

Mitigation: Review network access expectations and data-source availability before using the tracker in managed environments.

## Reference(s):

- [Dividend Premium Tracker on ClawHub](https://clawhub.ai/gykdly/skills/dividend-premium-tracker)
- [CSI H30269 Indicator XLS](https://oss-ch.csindex.com.cn/static/html/csindex/public/uploads/file/autofile/indicator/H30269indicator.xls)
- [ChinaBond Yield Data](https://yield.chinabond.com.cn/cbweb-czb-web/czb/moreInfo?locale=cn_ZH&nameType=1)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code, files, guidance]

**Output Format:** [Markdown guidance with bash commands, Python scripts, CSV files, and Excel workbooks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can update daily data, backfill a date range, generate Excel charts, and send Telegram alerts when configured.]

## Skill Version(s):

1.0.1 (source: frontmatter, release metadata, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
