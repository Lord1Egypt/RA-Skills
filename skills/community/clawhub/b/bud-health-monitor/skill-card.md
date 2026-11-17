## Description:

Monitor system health (RAM, disk, CPU, services), detect issues, and optionally attempt fixes for Raspberry Pi and home server environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stigg86](https://clawhub.ai/user/stigg86)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and home server maintainers use this skill to inspect RAM, disk, CPU, load, uptime, and process usage, with optional commands for continuous monitoring and automated remediation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fix mode can terminate processes and alter kernel cache behavior without strong user controls.

Mitigation: Use status or json mode for passive monitoring unless fix mode has explicit confirmation, dry-run behavior, allowlisted targets, corrected threshold logic, and clear logging.

Risk: Cron examples can automate remediation and may run with elevated privileges.

Mitigation: Review any scheduled command before enabling it, avoid running automated fix mode as root, and log remediation decisions for auditability.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stigg86/skills/bud-health-monitor)
- [Project homepage](https://github.com/stigg86/health-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce terminal health reports, monitoring commands, cron examples, and machine-readable JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
