## Description: <br>
Configure, repair, and validate OpenClaw scheduled outbound delivery to Feishu for reminders, recurring status reports, morning summaries, and failed proactive delivery repairs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timyao61-max](https://clawhub.ai/user/timyao61-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create, repair, and validate OpenClaw cron jobs that send proactive user-visible Feishu messages with explicit routing and smoke tests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated cron commands can schedule real recurring Feishu messages to user-visible recipients. <br>
Mitigation: Use test recipients first, replace placeholders with intended account and recipient values, confirm the message text and language, and review the command before running it. <br>
Risk: Fallback or internal cron routes can appear successful without delivering a Feishu message. <br>
Mitigation: Use explicit Feishu routing and validate with a one-shot smoke test plus cron run status before relying on delivery. <br>


## Reference(s): <br>
- [Validated Feishu cron delivery pattern](references/validated-pattern.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated OpenClaw cron commands with Feishu account and recipient placeholders.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
