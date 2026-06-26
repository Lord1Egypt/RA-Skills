## Description: <br>
Generate trading signals for stocks, indices, crypto, commodities, and forex using TradingView data and technical indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiescherbot-collab](https://clawhub.ai/user/aiescherbot-collab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run technical market analysis, generate buy and sell signals, and monitor configured assets for alert-worthy changes. It is intended for trading-signal assistance rather than autonomous financial decision-making. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send trading reports through Resend using local credentials and a default alert email. <br>
Mitigation: Remove or replace the default alert email and provide Resend credentials only when email delivery is intended. <br>
Risk: Continuous monitoring can poll market data on a schedule and send repeated alerts. <br>
Mitigation: Run monitor.js only when continuous polling is intended, review the configured interval, and stop the process when monitoring is no longer needed. <br>
Risk: Local signal history may be retained in .signal-state.json. <br>
Mitigation: Review, clear, or delete .signal-state.json when local signal history should not be retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aiescherbot-collab/aiescher-trading-signals) <br>
- [Asset configuration](references/assets.json) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Console text, HTML email reports, and Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist local signal history in .signal-state.json and may send email alerts when configured with Resend credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
