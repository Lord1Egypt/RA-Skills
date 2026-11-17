## Description:

BigA helps agents analyze A-share stocks by combining real-time quotes, technical timing scores, basic screening, catalyst searches, and scheduled Markdown push alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kobenfang](https://clawhub.ai/user/kobenfang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to monitor A-share markets, maintain a focused stock pool, generate buy, hold, sell, and timing signals, and send scheduled market-analysis updates. The outputs should be treated as informational investment analysis, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring scheduled jobs can send market-analysis messages automatically.

Mitigation: Verify the cron schedules, destination channel, target recipient, and timeout settings before installing, and remove scheduled jobs when alerts are no longer needed.

Risk: The skill produces buy, hold, sell, and timing signals that could be mistaken for personalized financial advice.

Mitigation: Treat all outputs as informational analysis, review the underlying market data and assumptions, and make investment decisions independently.

Risk: DSH setup references an unpinned BigTimer GitHub install.

Mitigation: Review and pin the BigTimer dependency or install only from a trusted, verified source before enabling DSH scheduling.

Risk: Broad triggers can cause the skill to run stock scans and send messages when users mention common A-share terms.

Mitigation: Confirm that trigger behavior is acceptable for the workspace and disable or narrow scheduled alerts if the volume is too high.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kobenfang/skills/biga)
- [Publisher profile](https://clawhub.ai/user/kobenfang)
- [technical-timing-score.md](artifact/references/technical-timing-score.md)
- [cron-templates.json](artifact/references/cron-templates.json)
- [cron-install-shell.sh](artifact/references/cron-install-shell.sh)
- [user-preferences.md](artifact/references/user-preferences.md)
- [sector-matrix.md](artifact/references/sector-matrix.md)
- [Shenzhen Stock Exchange trading calendar API](http://www.szse.cn/api/report/exchange/onepersistenthour/monthList?month={ym})
- [Tencent quote API](http://qt.gtimg.cn/q={symbol})
- [Sina daily K-line API](http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis, JSON scanner output, and shell commands for scheduled alerts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May split long alert text into multiple message segments; scheduled jobs use Asia/Shanghai trading-day timing.]

## Skill Version(s):

6.0.21 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
