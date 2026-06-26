## Description: <br>
Binance Alpha new coin launch detector that uses the Binance WebSocket !miniTicker@arr stream to detect new trading pairs and alert when symbols have a valid opening price. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manifoldor](https://clawhub.ai/user/manifoldor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, traders, and operators use this skill to monitor public Binance spot market streams for newly appearing trading pairs, review alert history, and inspect monitor status from the terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to Binance WebSocket and REST endpoints during monitoring. <br>
Mitigation: Run it only in environments where outbound access to Binance is allowed, or contain/block network access according to local policy. <br>
Risk: The skill stores known symbols and alert history under ~/.config/alpha. <br>
Mitigation: Review local filesystem policy before installation and remove or contain that state directory if persistent market-monitoring history is not desired. <br>


## Reference(s): <br>
- [Binance WebSocket API](https://binance-docs.github.io/apidocs/spot/en/#websocket-market-streams) <br>
- [Binance WebSocket API Reference](references/binance_ws.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/manifoldor/alpha) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions and terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script stores known symbols and alert history under ~/.config/alpha and keeps the most recent 100 alerts.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
