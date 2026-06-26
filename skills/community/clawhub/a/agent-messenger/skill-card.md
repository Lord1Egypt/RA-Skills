## Description: <br>
Send batch messages to OpenClaw agents across Telegram, Discord, or other channels with delivery tracking and retry logic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cheben77](https://clawhub.ai/user/cheben77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to broadcast messages, health checks, and workflow triggers to OpenClaw agents through Telegram-oriented helper scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses stored Telegram bot credentials and a hardcoded Telegram user ID by default. <br>
Mitigation: Change or remove the hardcoded user ID, verify bot tokens in /data/.openclaw/openclaw.json, and avoid sending secrets or sensitive operational details. <br>
Risk: The cron installer can create recurring outbound heartbeat messages. <br>
Mitigation: Run the cron installer only when recurring messages are intended, and confirm the schedule, logs, and removal steps before deployment. <br>
Risk: Outbound agent messages may reach unintended recipients if agent bindings or channel accounts are misconfigured. <br>
Mitigation: Review recipient agent IDs, Telegram account bindings, and message content before sending batch messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cheben77/agent-messenger) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown guidance with bash and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can send outbound Telegram messages and can install a recurring heartbeat cron job when invoked.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
