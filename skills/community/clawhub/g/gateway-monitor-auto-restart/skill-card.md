## Description:

Monitors the OpenClaw gateway every 3 hours, restarts it when unresponsive, diagnoses startup issues, and rotates logs with seven-day retention.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shirley6692026](https://clawhub.ai/user/shirley6692026)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators who run OpenClaw use this skill to install scheduled health checks that restart the gateway when it stops responding and preserve operational logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation creates an indefinite scheduled monitor that can restart or re-register the OpenClaw gateway.

Mitigation: Install only from a trusted, access-controlled path, inspect the crontab entry before use, and remove the cron entry manually if automatic recovery is no longer desired.

Risk: The monitor can kill matching gateway processes and has weak safeguards for shared or production systems.

Mitigation: Review gateway_monitor.sh before enabling it, confirm the process match targets only the intended gateway, and limit use to systems where automatic gateway recovery is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shirley6692026/skills/gateway-monitor-auto-restart)
- [README](artifact/README.md)
- [Skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may install a cron-based monitor and gateway restart workflow that writes logs under ~/.openclaw/logs.]

## Skill Version(s):

1.0.1 (source: evidence.release.version and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
