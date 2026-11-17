## Description:

Create portable OpenClaw cron health checks with deterministic scripts, config, validation, and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glucksberg](https://clawhub.ai/user/glucksberg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create or port a deterministic, script-only OpenClaw cron health kit for a specific instance. It helps audit scheduled OpenClaw jobs, system crons, logs, registry notes, callback notes, and delivery failures without changing scheduler state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring local checks may resolve diagnostic commands through an untrusted PATH.

Mitigation: Run the kit as a low-privilege account and harden command execution with a trusted PATH or a local derivative that verifies the intended openclaw, crontab, and systemctl binaries.

Risk: Cron lines, logs, registry notes, callback notes, and command output can contain sensitive or misleading content.

Mitigation: Review configured paths before scheduling, keep redaction enabled, validate redaction on real logs, and treat collected content as untrusted report data.

Risk: Instance-specific scheduler paths, delivery targets, and job metadata can be wrong when the kit is ported between OpenClaw servers.

Mitigation: Fill configuration only from the destination instance, run the checker manually once, and verify the script-only scheduled job after creation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/glucksberg/skills/cron-health-cron)
- [Setup Manual](references/setup-manual.md)
- [Report Format](references/report-format.md)
- [Porting Checklist](references/porting-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an instance-local OpenClaw cron health kit and a delivery-ready health report; routine checks are non-mutating and network-free.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
