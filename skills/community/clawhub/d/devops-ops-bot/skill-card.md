## Description:

Server health monitoring with alerts and auto-recovery. Checks CPU, memory, disk, and uptime with configurable thresholds. Sends Slack/Discord alerts and can auto-restart services on critical.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gruted](https://clawhub.ai/user/gruted)

### License/Terms of Use:


## Use Case:

Developers and operations engineers use this skill to run server health checks, tune warning and critical thresholds, send Slack or Discord alerts, and prepare recovery commands for critical service conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote installers and unpinned packages can execute changed code after publication.

Mitigation: Prefer a pinned npm package version or immutable container digest from a trusted release, and avoid the curl-to-shell installer path.

Risk: Webhook alerts may send operational server-health details to Slack or Discord destinations.

Mitigation: Enable webhook alerts only after reviewing what data is sent and restricting webhook access to the intended channel or workspace.

Risk: Automatic restart commands can affect production services during critical conditions.

Mitigation: Limit service-control permissions for restart commands and review each command before enabling auto-recovery.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gruted/skills/devops-ops-bot)
- [Project Repository](https://github.com/gruted/devops-ops-bot)
- [Landing Page](https://gruted.github.io/devops-ops-bot/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes examples for JSON status output, webhook alerting, cron scheduling, and restart-command configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
