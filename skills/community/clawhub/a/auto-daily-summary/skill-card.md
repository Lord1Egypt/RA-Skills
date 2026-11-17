## Description:

Sets up daily OpenClaw cron jobs that ask each configured agent to summarize completed work into its diary file at 23:30.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renchzhao](https://clawhub.ai/user/renchzhao)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to configure daily summary reminders across all available agents so each agent records completed work in its diary on a recurring schedule.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates persistent daily jobs for every detected OpenClaw agent.

Mitigation: Review the target agents before running the setup script, prefer a version with per-agent selection or dry-run support, and document how to remove created cron jobs.

Risk: Security evidence reports unsafe shell command construction that could run unintended local commands.

Mitigation: Run only in an environment where local command execution is acceptable, pin a reviewed version, and prefer an implementation that avoids shell=True and validates agent, workspace, and timezone values.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent daily cron jobs for detected OpenClaw agents when the setup script is run.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
