## Description:

Provides multi-timeframe Chan theory analysis for stocks, indexes, and XAUUSD using market data, CZSC-style structures, MACD, moving averages, Fibonacci levels, and generated charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouyuzhy](https://clawhub.ai/user/zhouyuzhy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate structured Chan theory market analysis, trading scenario classification, strategy guidance, and chart artifacts for equities, indexes, and XAUUSD.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated financial analysis can be incorrect, incomplete, or misleading.

Mitigation: Treat outputs as informational analysis only, verify market data and assumptions independently, and review conclusions before acting on them.

Risk: The skill may read market-data credentials and use an existing Baidu Netdisk authorization to upload generated artifacts.

Mitigation: Use scoped credentials, disable or remove cloud upload when not required, and review the destination paths before running the skill.

Risk: The security evidence calls out an exposed Tushare token.

Mitigation: Rotate the exposed token and configure market-data credentials through environment variables or a secrets manager before use.

Risk: Broad routing and persistence behavior may cause the skill to run or update stored analysis in more situations than expected.

Mitigation: Review triggers and persistence instructions before installation, and install only in workspaces where these behaviors are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhouyuzhy/skills/chan-stock-analysis)
- [CZSC Framework](https://github.com/waditu/czsc)
- [itick Forex Kline API](https://api.itick.org/forex/kline)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown analysis report with optional chart files and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save local reports and charts and upload generated analysis artifacts to Baidu Netdisk when configured.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
