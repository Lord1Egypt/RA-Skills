## Description:

Production-grade health monitoring, alerting, and service management for OpenClaw agents. Monitor URLs, auto-restart services, get Telegram alerts, track uptime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrsmithai](https://clawhub.ai/user/mrsmithai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to set up local health checks, uptime metrics, Telegram alerts, task board tracking, and optional service restart workflows for OpenClaw agent services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic recovery can run broad configured shell commands on a recurring schedule.

Mitigation: Enable auto-recovery only after reviewing each restart command, replacing free-form commands with allowlisted commands, restricting configuration edits, and avoiding broad sudo privileges.

Risk: Telegram alerting can expose operational details and depends on bot tokens stored in local configuration.

Mitigation: Protect Telegram credentials with restrictive file permissions or a credential store and avoid sending sensitive incident details in alert text.

Risk: The monitor writes operational logs, state, and metrics under ~/.agent-ops.

Mitigation: Review retention settings, file permissions, and cleanup behavior before running the monitor on production systems.

## Reference(s):

- [Agent Ops Kit ClawHub page](https://clawhub.ai/mrsmithai/skills/agent-ops-kit)
- [Publisher profile](https://clawhub.ai/user/mrsmithai)
- [Sample configuration](references/sample-config.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may lead users to create local configuration, logs, state, and metrics under ~/.agent-ops and to schedule recurring health checks.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
