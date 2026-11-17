## Description:

Monitors configured A-share stock holdings for stop-loss, support breakdown, target price, abnormal daily movement, profit and loss, and moving-average deviation alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jdvrommel](https://clawhub.ai/user/jdvrommel)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure and run a Python monitor for A-share holdings, producing status summaries and alerts when configured price or movement thresholds are reached. It is intended for informational monitoring and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market data is fetched over unauthenticated HTTP, which can expose the monitor to tampered or unreliable price data.

Mitigation: Use an authenticated HTTPS market-data source before relying on alerts for financial decisions.

Risk: The script writes holding state to a predictable temporary file.

Mitigation: Move state to a private user-owned path with restrictive permissions.

Risk: Cron scheduling can repeatedly run the monitor with the permissions of the configured user.

Mitigation: Run it as a non-root user and review the cron entry before enabling scheduled execution.

Risk: Generated alerts can be mistaken for investment advice.

Mitigation: Treat alerts as informational and verify holdings, market data, and risk thresholds independently.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jdvrommel/skills/a-stock-holding-monitor)
- [Publisher profile](https://clawhub.ai/user/jdvrommel)
- [Sina Finance](http://finance.sina.com.cn)
- [Sina quote endpoint](http://hq.sinajs.cn/list={code})
- [Sina K-line endpoint](http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text console summaries and alerts, plus a JSON state file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes latest holding status to /tmp/holding_check.json and returns a nonzero exit code when alert signals are present.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
