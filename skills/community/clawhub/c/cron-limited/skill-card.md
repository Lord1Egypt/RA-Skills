## Description:

Creates limited-run recurring OpenClaw cron reminders that clean themselves up after a set number of executions, and supports lunar-calendar birthday reminders with yearly repeats, reminder times, and advance notice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuzhiyongcn-coder](https://clawhub.ai/user/yuzhiyongcn-coder)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to schedule reminders that repeat for a limited number of runs and then stop automatically. They can also configure lunar birthday reminders, including yearly recurrence, a reminder time, and reminders sent a specified number of days in advance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted reminder arguments can execute code as the current user.

Mitigation: Review or patch the script before installation; validate inputs and pass user data to Python safely.

Risk: The skill creates persistent scheduled jobs and local reminder records containing message and recipient data.

Mitigation: Review scheduled jobs and stored reminder records, and prefer a patched version with list, remove, and purge controls.

Risk: The script uses an interpreter path under /tmp.

Mitigation: Use a trusted, stable Python environment instead of relying on an interpreter in /tmp.

## Reference(s):

- [Cron Limited release page](https://clawhub.ai/yuzhiyongcn-coder/skills/cron-limited)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent scheduled jobs and local reminder records when used.]

## Skill Version(s):

1.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
