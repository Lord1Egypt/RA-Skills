## Description: <br>
Sleep better tonight - personalized wind-down routine, breathing exercises, bedtime stories, and sleep hygiene tips. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiajiaoy](https://clawhub.ai/user/jiajiaoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use Daily Sleep to receive sleep coaching prompts, bedtime wind-down guidance, daily sleep tips, and optional recurring morning and evening reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring sleep reminders may be disruptive if enabled unintentionally or no longer wanted. <br>
Mitigation: Enable reminders only by explicit user choice and use the provided off command to disable morning and evening scheduled pushes. <br>
Risk: A userId is stored with simple reminder preferences. <br>
Mitigation: Use a non-sensitive identifier and avoid putting personal or confidential information in the userId. <br>
Risk: Broad trigger phrases may activate sleep coaching in unintended conversations. <br>
Mitigation: Narrow trigger phrases before deployment if accidental activation would be disruptive. <br>


## Reference(s): <br>
- [Daily Sleep on ClawHub](https://clawhub.ai/jiajiaoy/daily-sleep) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can emit OpenClaw cron add/remove control messages for opt-in sleep reminders.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
