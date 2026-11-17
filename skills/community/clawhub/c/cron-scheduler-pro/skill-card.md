## Description:

定时调度专家 helps AI agents manage local recurring jobs with timezone locking, next-run preview, one-time job cleanup, concurrent write protection, retry, and circuit-breaker guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to turn recurring-task requests, reminders, health checks, reports, and local workflow jobs into auditable schedules that an agent can manage. It is intended for local-first scheduling workflows where users review job definitions, storage paths, timezones, and downstream task credentials before unattended execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent toward persistent local scheduled jobs and future task execution.

Mitigation: Review each job definition, storage path, timezone, cleanup policy, and confirmation boundary before allowing unattended execution.

Risk: Scheduled tasks may inherit command, file, or API authority from the executing agent or downstream task.

Mitigation: Limit scheduled work to scoped, low-risk actions and review any credentials or external API use required by the downstream task.

Risk: The security verdict is suspicious due to broad activation scope, persistent jobs, auto-cleanup behavior, and mixed API-key guidance.

Mitigation: Install only when a local scheduler is desired, keep high-stakes actions out of scope, and require user review until confirmation controls are tightened.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/cron-scheduler-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, code snippets, JSON examples, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local scheduling guidance and job-management patterns; scheduled jobs may create or update local cron memory files when implemented by an agent.]

## Skill Version(s):

1.0.2 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
