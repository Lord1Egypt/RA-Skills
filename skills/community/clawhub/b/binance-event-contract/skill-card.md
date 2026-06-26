## Description: <br>
Continuously gathers Binance BTCUSDT and ETHUSDT event-contract market data and produces advisory signal, ICT-structure, risk, execution-tracking, and reporting outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[acwxpunh](https://clawhub.ai/user/acwxpunh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Traders, analysts, and agent operators use this skill system to monitor Binance BTCUSDT and ETHUSDT event-contract conditions, generate advisory trade signals, check risk limits, track signal status, and produce performance reports. It is advisory-oriented and its outputs require human review before any trading decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to run continuously and poll Binance data every minute, which may create operational load or unwanted background activity. <br>
Mitigation: Install it only when continuous crypto-market monitoring is intended, and confirm how to disable or pause polling before activation. <br>
Risk: The skill produces financial trading signals, win-rate claims, position-size guidance, and P&L tracking that may be mistaken for guaranteed trading advice. <br>
Mitigation: Treat all signal, win-rate, and position-size outputs as unverified financial analysis requiring independent human review. <br>
Risk: Reports and alerts may be sent to Feishu, which could expose trading-analysis details or performance logs. <br>
Mitigation: Confirm exactly what data is sent to Feishu and where execution logs and caches are stored before using the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/acwxpunh/binance-event-contract) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/acwxpunh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style reports, advisory signal summaries, risk-check results, status logs, alerts, and installation or trigger commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs focus on Binance BTCUSDT and ETHUSDT event-contract workflows and may include prices, targets, stop-loss levels, position-size guidance, P&L tracking, and Feishu alert content.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
