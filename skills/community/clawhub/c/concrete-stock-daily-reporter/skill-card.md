## Description:

Generates and optionally sends daily custom stock reports with market prices, KDJ indicators, rankings, key signals, and summary statistics for user-provided stock codes and names.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenhulove333](https://clawhub.ai/user/wenhulove333)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate daily watchlist stock reports from supplied stock code/name pairs, including prices, KDJ indicators, rankings, and key signal summaries. Users may also invoke its sending and scheduling workflow when they have reviewed and configured the Feishu recipient and cron behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sending workflow can transmit the user's watchlist and report contents to a fixed Feishu recipient.

Mitigation: Replace the Feishu target with a user-controlled, verified destination before using the send script, or generate reports locally without sending them.

Risk: Cron scheduling can create recurring execution that continues after initial setup.

Mitigation: Review any crontab entry before enabling it, scope the schedule intentionally, and remove or disable the entry when reports are no longer needed.

Risk: Market data integrity is weakened by disabled TLS verification and use of plaintext HTTP for one data source.

Mitigation: Treat fetched market data as untrusted, verify important results with trusted sources, and prefer validated HTTPS data paths where available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wenhulove333/skills/concrete-stock-daily-reporter)
- [ClawHub publisher profile](https://clawhub.ai/user/wenhulove333)
- [Sina Finance market data endpoint](https://hq.sinajs.cn)
- [Eastmoney K-line API endpoint](http://push2his.eastmoney.com/api/qt/stock/kline/get)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text stock report with command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied stock code/name pairs; optional Feishu sending and cron scheduling require user review before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
