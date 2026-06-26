## Description: <br>
Creates scheduled reminders through cron jobs and delivers them to the current Telegram chat through system events, including multi-agent reminder routing through a main agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alex3alex](https://clawhub.ai/user/alex3alex) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agent users and operators use this skill to create one-time, recurring, or interval-based reminders that are delivered to Telegram chats. It is also intended for multi-agent setups where non-main agents route scheduled reminder messages through a main agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent scheduled jobs may continue sending reminders after they are no longer wanted. <br>
Mitigation: Periodically review and remove old cron jobs, HEARTBEAT reminder rules, and stored chat IDs. <br>
Risk: Broad Telegram message-sending authority can send reminders to unintended recipients or through unintended bot accounts. <br>
Mitigation: Use verified recipient chat IDs, restrict allowed accountId and target values, and confirm reminders before creation. <br>
Risk: Bot tokens, chat IDs, or routing details may be exposed through logs or memory. <br>
Mitigation: Keep bot tokens out of logs and memory, and store only the minimum recipient and routing information required. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reminder setup instructions, cron job payload examples, heartbeat configuration guidance, and message-tool routing guidance.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
