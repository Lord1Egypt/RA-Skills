## Description: <br>
Manage Apple Reminders via the remindctl CLI for time-anchored or place-anchored tracking that does not belong on the calendar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luisbueno](https://clawhub.ai/user/luisbueno) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who use Apple Reminders can have an agent capture, review, edit, and complete reminders through remindctl, especially for due dates, recurrence, location triggers, and quick list checks. The skill is scoped for reminder management rather than calendar scheduling or durable knowledge storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change iCloud-synced Apple Reminders that appear across the user's Apple devices. <br>
Mitigation: Install it only when agent-managed reminders are desired, and have the agent summarize parsed JSON results after reminder changes. <br>
Risk: The skill depends on the external remindctl Homebrew tool and macOS Reminders Automation permission. <br>
Mitigation: Verify the remindctl installation source and authorization status before relying on the skill for reminder changes. <br>
Risk: Some durable reminder context may be mirrored into Open Brain when the skill judges that context useful later. <br>
Mitigation: Mirror only durable facts or protocols, and reference the reminder ID prefix so users can audit the connection. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luisbueno/apple-reminders-remindctl) <br>
- [Publisher profile](https://clawhub.ai/user/luisbueno) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and human summaries of JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses non-interactive remindctl commands and expects JSON output from read operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
