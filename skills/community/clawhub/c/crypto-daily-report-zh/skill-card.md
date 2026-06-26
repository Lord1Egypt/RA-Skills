## Description: <br>
Generate and send cryptocurrency daily reports with market overview, fear and greed index, liquidation data, economic calendar, and news aggregation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RenYuKe-CN](https://clawhub.ai/user/RenYuKe-CN) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Crypto analysts, community operators, and developers use this skill to generate Chinese-language daily crypto market briefings and optionally schedule delivery to Telegram or Discord channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring Telegram report delivery can be enabled with weak confirmation and unclear removal guidance. <br>
Mitigation: Review before installing, replace example Telegram targets with intended channels, confirm the schedule before enabling cron, and document how to remove the scheduled job. <br>
Risk: Delivery credentials or bot permissions could expose reports to unintended channels if over-privileged. <br>
Mitigation: Use least-privileged bot and channel credentials for delivery. <br>


## Reference(s): <br>
- [Data Sources Reference](data-sources.md) <br>
- [Report Template](report-template.txt) <br>
- [Alternative.me Fear and Greed API](https://api.alternative.me/fng/?limit=2) <br>
- [Cointelegraph RSS](https://cointelegraph.com/rss) <br>
- [TokenInsight RSS](https://tokeninsight.com/rss/news) <br>
- [Incrypted Calendar](https://incrypted.com/en/calendar/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese-language Markdown-style report with optional shell commands and JSON data from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include scheduled Telegram or Discord delivery setup; market data depends on external sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
