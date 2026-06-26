## Description: <br>
ETF volatility monitor that tracks ETF price changes and prints alerts when configured thresholds are exceeded. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zitjubiz](https://clawhub.ai/user/zitjubiz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to monitor a configurable list of ETFs, fetch public quote data, and emit alerts when price movement exceeds a chosen percentage threshold. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to Tencent Finance for ETF quote data. <br>
Mitigation: Install and run it only in environments where this network access is acceptable. <br>
Risk: ETF alerts can be mistaken for financial advice or fully current market data. <br>
Mitigation: Treat alerts as monitoring signals only, verify against authoritative market sources, and do not use them as financial advice. <br>
Risk: Cron or notification integrations can create unwanted execution frequency or message destinations. <br>
Mitigation: Configure scheduling and notification delivery explicitly so frequency and destinations remain under operator control. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zitjubiz/etf-monitor) <br>
- [Tencent Finance quote endpoint example](http://qt.gtimg.cn/q=sz159985) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON object printed to stdout with an alerts array; operational guidance is documented as Markdown and shell examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, the requests package, and outbound access to Tencent Finance; ETF symbols and alert threshold are configured in the script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and release changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
