## Description: <br>
Tamper-resistant audit watchdog for Clawdbot agents. Detects and logs suspicious filesystem activity with HMAC-chained evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apollostreetcompany](https://clawhub.ai/user/apollostreetcompany) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators running Clawdbot on Linux use Clauditor to install, configure, and operate a systemd watchdog that records tamper-evident audit logs and digest reports for suspicious filesystem and command activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer sets up a privileged, persistent Linux systemd monitor with broad host visibility. <br>
Mitigation: Install only when this monitoring posture is intentional, inspect every sudo command first, and confirm uninstall coverage for services, user, keys, and logs. <br>
Risk: The artifact uses stealth-oriented service and log paths that can obscure what is running on the host. <br>
Mitigation: Prefer transparent service names where operationally possible and document the installed binary, unit files, config, key, and log locations. <br>
Risk: The security guidance notes missing dist assets that affect installation trust. <br>
Mitigation: Verify required dist assets from a trusted source before starting the service or relying on generated configuration. <br>


## Reference(s): <br>
- [Clauditor ClawHub release page](https://clawhub.ai/apollostreetcompany/clauditor) <br>
- [Clauditor project homepage](https://github.com/apollostreetcompany/clauditor) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with bash commands; CLI subcommands can emit JSON or Markdown digest reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Linux with systemd plus cargo for building; installation steps require root privileges.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
