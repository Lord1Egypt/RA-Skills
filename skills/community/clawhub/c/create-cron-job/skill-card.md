## Description:

Create and configure OpenClaw cron jobs with correct scheduling, execution modes, and delivery patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kjvarga](https://clawhub.ai/user/kjvarga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create and document OpenClaw scheduled tasks, including recurring jobs, one-shot reminders, execution modes, and delivery settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent scheduled jobs.

Mitigation: Review the schedule, agent binding, delivery target, webhook URL, and one-shot deletion settings before allowing a job to run.

Risk: The skill may force immediate execution during testing.

Mitigation: Confirm whether immediate execution is intended before running test commands such as forced cron execution.

## Reference(s):

- [Create Cron Job on ClawHub](https://clawhub.ai/kjvarga/skills/create-cron-job)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and a configuration checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces proposed OpenClaw cron commands and documentation guidance; commands require review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
