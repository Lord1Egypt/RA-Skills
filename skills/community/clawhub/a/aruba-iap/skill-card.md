## Description:

Provides Aruba Instant AP configuration management with baseline capture, rollback support, health monitoring, device discovery, configuration snapshots, SSID management, and safe configuration changes through interactive config mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scsun1978](https://clawhub.ai/user/scsun1978)

### License/Terms of Use:

MIT

## Use Case:

Network administrators and infrastructure engineers use this skill to inspect, back up, monitor, and safely change Aruba Instant AP configurations. It is intended for operational workflows such as SSID management, configuration snapshots, health checks, and rollback planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make high-impact network-management changes to Aruba Instant AP devices.

Mitigation: Review planned changes, run dry-run workflows first, keep current backups, and apply changes only from a controlled administrator environment.

Risk: Credential and artifact handling may expose sensitive device, network, or secret material if used carelessly.

Mitigation: Prefer SSH keys with host-key verification, avoid plaintext secrets files and password flags for real credentials, keep output directories private, and do not commit generated artifacts.

Risk: Installation behavior and dependency management require review before use on shared systems.

Mitigation: Inspect the code before installation and avoid running install.sh until wrapper overwrite and dependency-pinning concerns are addressed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scsun1978/skills/aruba-iap)
- [Aruba Networks](https://www.arubanetworks.com)
- [Aruba IAP Configuration Changes](artifact/docs/CONFIG-CHANGES.md)
- [iapctl Quick Reference Card](artifact/docs/QUICK-REFERENCE.md)
- [Quick Start: Aruba IAP Configuration Changes](artifact/docs/QUICKSTART-CONFIG.md)
- [Aruba IAP Best Practices](artifact/references/best_practices.md)
- [Aruba IAP CLI Complete Command Reference](artifact/references/cli_commands.md)
- [Aruba IAP Troubleshooting Guide](artifact/references/troubleshooting.md)
- [iapctl - Aruba IAP Configuration Management CLI](artifact/iapctl/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create configuration, backup, diff, apply, verification, and monitoring artifacts when the generated commands are run.]

## Skill Version(s):

1.2.0 (source: server release evidence and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
