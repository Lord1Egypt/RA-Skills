## Description:

Provides durable, SQLite-backed scheduling guidance for OpenClaw shell and agent workflows with retries, approvals, run history, and gateway-aware dispatch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amittell](https://clawhub.ai/user/amittell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to decide when and how to install and operate openclaw-scheduler for durable OpenClaw job scheduling, multi-step workflows, approvals, and CLI-based run auditing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned third-party global package and registers a persistent background service.

Mitigation: Pin and verify the package version, review the generated plist before bootstrapping it, and document pause, removal, and audit procedures before enabling unattended jobs.

Risk: Scheduled workflows can run shell and agent jobs, including privileged commands.

Mitigation: Avoid running jobs as root, restrict shell commands to reviewed operations, and require approval steps before remediation actions.

## Reference(s):

- [Durable Scheduler ClawHub listing](https://clawhub.ai/amittell/skills/durable-scheduler)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include launchd setup commands, scheduler CLI examples, workflow definitions, and operational cautions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
