## Description:

Daily Summary generates a concise daily work summary from local OpenClaw memory and Chrome/Edge browsing history for Feishu delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppop0uuiu](https://clawhub.ai/user/ppop0uuiu)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to create a one-sentence summary of the day's work from local memory and recent browser activity. It can be run manually or scheduled to support recurring Feishu status updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads sensitive local activity data from OpenClaw memory and Chrome/Edge browsing history.

Mitigation: Review the data access before installation and prefer manual runs until the skill documents explicit opt-in controls.

Risk: The skill can be scheduled as a recurring Feishu-channel task.

Mitigation: Confirm the schedule and channel before enabling automation, and require clear removal steps for any recurring task.

Risk: The skill appends generated summaries to persistent OpenClaw memory.

Mitigation: Review generated summaries before relying on them and keep a way to inspect or remove appended memory entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ppop0uuiu/skills/daily-summary-cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Plain text summary appended to a Markdown memory file, with optional Feishu delivery configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local OpenClaw memory and Chrome/Edge browsing history, append to the daily memory file, and run through a scheduled Feishu channel task.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
