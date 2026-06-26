## Description: <br>
A股模拟盘交易与回测技能，用于启动模拟交易服务、管理多账户、执行限价单或市价单、撤单、查询资金持仓、验证A股交易规则并运行回测。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shouldnotappearcalm](https://clawhub.ai/user/shouldnotappearcalm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run a local A-share paper-trading simulator, manage simulated accounts and orders, inspect positions and trades, and validate trading-rule behavior before relying on simulated results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local paper-trading service stores simulated account, order, trade, and history data on the user's machine. <br>
Mitigation: Use the default user data directory, protect local machine access, and remove the local database when simulated trading history is no longer needed. <br>
Risk: The localhost service could be exposed beyond the intended machine if it is bound to a non-local interface. <br>
Mitigation: Keep the service bound to 127.0.0.1 unless intentional network exposure is required and reviewed. <br>
Risk: Market quotes and history are fetched from public finance-data providers. <br>
Mitigation: Use the skill only when outbound requests to public finance-data providers are acceptable for the user's environment. <br>
Risk: The optional macOS launchd setup can restart the service automatically after login. <br>
Mitigation: Install the launchd option only when persistent background operation is desired, and use the provided control script to check status or stop the service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shouldnotappearcalm/a-share-paper-trading) <br>
- [Eastmoney Finance](https://finance.eastmoney.com) <br>
- [Sina Finance K-line API](https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData) <br>
- [Tencent Finance quote endpoint](https://qt.gtimg.cn/q=) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI or service responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local CLI and localhost service interactions; CLI output can be requested as JSON for structured follow-up.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
