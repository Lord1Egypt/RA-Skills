## Description: <br>
Monitors A-share stock holdings for stop-loss, support-break, target-price, and abnormal-movement conditions, then reports alerts and suggested actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jdvrommel](https://clawhub.ai/user/jdvrommel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and investors use this skill to configure and run a local A-share holdings monitor that fetches market prices, calculates profit and loss, and flags configured alert conditions. It is intended for manual execution or scheduled cron checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured holdings and recent portfolio status may expose sensitive financial information, especially because the script writes status to /tmp/holding_check.json by default. <br>
Mitigation: Use a private user-owned output path with restrictive permissions before running the monitor on a shared or multi-user machine. <br>
Risk: Alert quality depends on the configured thresholds and availability of the external market-data source. <br>
Mitigation: Review stop-loss, support, target, and anomaly thresholds for the user portfolio, and treat generated alerts as monitoring signals rather than financial advice. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/jdvrommel/a-stock-holding-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/jdvrommel) <br>
- [Sina Finance quote endpoint](http://hq.sinajs.cn/list={code}) <br>
- [Sina Finance K-line data endpoint](http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Python configuration snippets and shell commands; runtime output is console text plus JSON status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes recent holding status to a local JSON file when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
