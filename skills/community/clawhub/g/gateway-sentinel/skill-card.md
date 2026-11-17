## Description:

Gateway Sentinel monitors an OpenClaw gateway with CLI and HTTP health checks, sends Telegram or Discord alerts, and runs graduated recovery actions including restart, doctor fix, daily snapshots, and optional git rollback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zurbrick](https://clawhub.ai/user/zurbrick)

### License/Terms of Use:


## Use Case:

Developers and operators use Gateway Sentinel to keep an OpenClaw gateway monitored, receive alerts, and attempt automated recovery when the gateway becomes unhealthy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a persistent per-user watchdog that can restart OpenClaw, run repair commands, and automatically commit unignored workspace changes.

Mitigation: Review the service configuration before installation, set `GUARDIAN_WORKSPACE` to the narrowest intended repository, and verify `.gitignore` coverage before enabling daily snapshots.

Risk: Optional rollback can run git reset behavior in the configured workspace when `GUARDIAN_ENABLE_ROLLBACK=true`.

Mitigation: Keep rollback disabled unless it has been tested in the target workspace, and maintain independent backups or recovery procedures.

Risk: Alert tokens and webhook URLs are supplied through environment configuration and could be exposed if stored or logged carelessly.

Mitigation: Protect `~/.openclaw/guardian.env`, rotate any exposed Telegram or Discord credentials, and consider moving logs and state out of `/tmp`.

## Reference(s):

- [Gateway Sentinel ClawHub page](https://clawhub.ai/zurbrick/skills/gateway-sentinel)
- [OpenClaw Guardian homepage](https://github.com/openclaw/openclaw-guardian)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include service install or uninstall commands, environment variable settings, and operational guidance for macOS launchd or Linux systemd.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
