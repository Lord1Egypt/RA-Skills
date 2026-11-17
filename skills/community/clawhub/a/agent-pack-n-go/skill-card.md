## Description:

Clone an OpenClaw Agent to a new Linux device by packaging configs, memory, skills, credentials, and related runtime setup, then transferring and deploying them over SSH.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aicodelion](https://clawhub.ai/user/aicodelion)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to migrate or clone a configured OpenClaw agent from one trusted Linux device to another, including agent configuration, memory, skills, credentials, and runtime setup. It supports device moves, backup snapshots, team setup replication, and local-to-cloud deployment workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The migration can copy sensitive credentials, tokens, OAuth data, SSH keys, memory, and agent configuration to another device.

Mitigation: Install and run only when both devices are fully trusted; exclude or regenerate SSH private keys where possible, encrypt the migration archive, and delete transferred archives and temporary files immediately after verification.

Risk: The workflow may request broad system access, including sudo-capable remote setup and temporary passwordless sudo.

Mitigation: Avoid NOPASSWD:ALL where possible, prefer limited or manually approved sudo operations, and remove any temporary sudoers entry after the clone is verified.

Risk: Restored cron entries, host mappings, proxy settings, and system service configuration may introduce unwanted behavior on the destination device.

Mitigation: Review cron entries, system configuration changes, proxy settings, service status, and skipped-permission automation before and after deployment.

## Reference(s):

- [OpenClaw Device Migration Operations Manual](references/migration-guide.md)
- [Troubleshooting Guide](references/troubleshooting.md)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [agent-life](https://agent-life.ai/)
- [OpenClaw Migration Guide](https://docs.openclaw.ai/install/migrating)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated migration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate a local migration archive, setup and deployment shell scripts, progress logs, checksums, and fallback migration instructions.]

## Skill Version(s):

2.3.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
