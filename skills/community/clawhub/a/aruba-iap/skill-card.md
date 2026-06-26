## Description: <br>
Comprehensive Aruba Instant AP configuration management with automatic baseline capture, rollback support, health monitoring, device discovery, configuration snapshots, SSID management, and safe configuration changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scsun1978](https://clawhub.ai/user/scsun1978) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Network administrators and infrastructure engineers use this skill to discover, monitor, snapshot, diff, apply, verify, and roll back Aruba Instant AP configuration changes through iapctl workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change live Aruba access-point configuration, which may disrupt network connectivity if applied without authorization or review. <br>
Mitigation: Use it only in a controlled administrative environment, review generated changes, prefer dry-run mode for critical changes, keep backups, and maintain a tested recovery plan. <br>
Risk: The skill handles network credentials and may create backups or monitoring output that contain sensitive operational details. <br>
Mitigation: Prefer SSH keys, avoid command-line passwords and default helper-script credentials, use secret references, and store outputs in protected directories. <br>
Risk: Post-apply verification can time out even when configuration changes have been applied. <br>
Mitigation: Retry verification after a short wait and confirm device state before continuing with additional changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/scsun1978/aruba-iap) <br>
- [Skill README](artifact/README.md) <br>
- [Configuration Changes Guide](artifact/docs/CONFIG-CHANGES.md) <br>
- [Quick Start Configuration Guide](artifact/docs/QUICKSTART-CONFIG.md) <br>
- [Quick Reference](artifact/docs/QUICK-REFERENCE.md) <br>
- [Aruba IAP Best Practices](artifact/references/best_practices.md) <br>
- [Aruba IAP CLI Command Reference](artifact/references/cli_commands.md) <br>
- [Aruba IAP Troubleshooting Guide](artifact/references/troubleshooting.md) <br>
- [Aruba Networking](https://www.arubanetworks.com) <br>
- [Aruba Technical Documentation](https://arubanetworking.hpe.com/techdocs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce iapctl command sequences, dry-run/apply/rollback workflows, and local JSON artifacts for network-device administration.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact/iapctl/pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
