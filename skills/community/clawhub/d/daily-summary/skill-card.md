## Description:

Daily Summary generates a dated learning and progress summary with task status, next plans, and token usage statistics from local OpenClaw status data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asterisk622](https://clawhub.ai/user/asterisk622)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create a daily Markdown summary of work completed, task status, follow-up plans, and token consumption for a local OpenClaw workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated daily summary may expose token usage totals or work-summary details that are sensitive in some environments.

Mitigation: Review the generated memory/YYYY-MM-DD.md file before sharing it outside the local workspace.

Risk: The skill runs openclaw status --json locally and writes a dated Markdown file in the workspace memory directory.

Mitigation: Install and run it only in workspaces where local OpenClaw status access and memory-file updates are expected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asterisk622/skills/daily-summary)
- [Publisher profile](https://clawhub.ai/user/asterisk622)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown daily summary plus a brief text response with token totals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates memory/YYYY-MM-DD.md in the user's local OpenClaw workspace.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
