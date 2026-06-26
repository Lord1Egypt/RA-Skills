## Description: <br>
Routes Discord notifications with deterministic rules and local AI formatting while supporting message updates, deduplication, and recovery workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bhupendrafire-ai](https://clawhub.ai/user/bhupendrafire-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to design Discord webhook dispatchers for monitoring, alerting, dashboard-style message updates, and recovery of missed notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recovery workflows can reset local state and force-send or update external Discord notifications. <br>
Mitigation: Use manual approval and dry-run previews before Heal Mode or backlog replays, back up state files, and cap resend volume. <br>
Risk: Webhook secrets and local configuration files may be exposed or misused if stored with broad permissions. <br>
Mitigation: Use dedicated low-privilege webhooks, protect local configuration files, and make scheduled tasks easy to audit and disable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bhupendrafire-ai/discord-ai-dispatcher) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, Code] <br>
**Output Format:** [Markdown guidance with configuration and scripting patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include operational steps for webhook routing, state tracking, scheduling, and recovery workflows.] <br>

## Skill Version(s): <br>
1.7.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
