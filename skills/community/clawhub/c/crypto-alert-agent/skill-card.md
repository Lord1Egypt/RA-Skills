## Description: <br>
A proactive agent that monitors cryptocurrency prices, tracks your portfolio, and sends alerts via Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Vitja1988](https://clawhub.ai/user/Vitja1988) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to track cryptocurrency prices, manage simple portfolio holdings, and receive Telegram alerts when configured price conditions are met. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio holdings and alert details may be exposed through local skill state or Telegram notifications. <br>
Mitigation: Use only non-sensitive portfolio information, protect local credentials, and install only if Telegram delivery is acceptable for this data. <br>
Risk: Notifications can be sent to the wrong destination if the Telegram chat ID or bot configuration is incorrect. <br>
Mitigation: Verify the destination chat ID and protect the Telegram bot token before enabling alerts. <br>
Risk: Scheduled execution can repeatedly run the skill's shell entry point. <br>
Mitigation: Inspect the run.sh implementation before adding a cron job or persistent agent loop. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Vitja1988/crypto-alert-agent) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Vitja1988) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and cron code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Telegram notifications and command-line responses may include price, alert, and portfolio information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
