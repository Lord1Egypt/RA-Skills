## Description:

Deployment Kit helps developers deploy and maintain VPS services with shell scripts for build, restart, health checks, systemd service templates, heartbeat monitoring, and Telegram alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[northcap-group](https://clawhub.ai/user/northcap-group)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prepare deployment, restart, monitoring, and alerting commands and configuration for services they own on VPS or staging hosts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Service restart and process-kill commands can interrupt running workloads or affect unintended processes.

Mitigation: Install only on owned VPS or staging hosts, review the scripts before use, restrict service names to an allowlist, and remove or replace the pkill -f fallback before production use.

Risk: Sudo-based systemd restarts can affect host-level services beyond the target application.

Mitigation: Scope sudoers permissions to specific approved service units and require dry-run or confirmation workflows for deployment actions.

Risk: Telegram bot credentials and runtime state may be exposed through fragile storage or command invocation patterns.

Mitigation: Store alert credentials in a private file with restrictive permissions, use a private runtime directory for logs and heartbeat files, and prefer an alerting method that avoids exposing tokens in process arguments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/northcap-group/skills/deployment-kit)
- [Telegram API endpoint used by alerting metadata](https://api.telegram.org)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown with inline shell commands and script/configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deployment guidance that may reference systemd, sudo, curl, nohup, setsid, heartbeat files, and Telegram alert credentials.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
