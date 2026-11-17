## Description:

Configures scheduled agent jobs for one-time reminders, recurring cron tasks, background automation, chat-channel delivery, and execution-log review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to create, configure, and inspect scheduled automation for reminders, recurring operational tasks, and agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent scheduled automation can continue acting after initial setup.

Mitigation: Install only from a trusted publisher, review each scheduled job before enabling it, limit job permissions, and define cancellation and retention controls.

Risk: External message delivery can expose private email, calendar, project, or business data.

Mitigation: Avoid scheduling sensitive-data tasks unless recipients, channels, logs, and retention are explicitly controlled.

Risk: Execution logs can retain sensitive task details.

Mitigation: Review log locations and retention settings, restrict log access, and avoid placing secrets or private data in scheduled messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/cron-scheduler-setup)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cron expressions, time zones, delivery-channel settings, and execution-log guidance.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
