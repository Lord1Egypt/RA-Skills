## Description:

Use when asked to manage UniFi network - list/restart/upgrade devices, block/unblock clients, manage WiFi networks, control PoE ports, manage traffic rules, create guest vouchers, or any UniFi controller task. Works with UDM Pro/SE, Dream Machine, Cloud Key Gen2+, or self-hosted controllers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[araa47](https://clawhub.ai/user/araa47)

### License/Terms of Use:


## Use Case:

Developers, operators, and network administrators use this skill to let an agent prepare and run UniFi controller administration commands for devices, clients, WLANs, switch ports, traffic rules, firewall objects, vouchers, and controller health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can grant an agent broad administrative control over a UniFi controller.

Mitigation: Use the narrowest dedicated local account possible and avoid Super Admin unless it is truly required.

Risk: Credentials may be exposed through environment files or command-line use of sensitive values such as WiFi passwords.

Mitigation: Protect or avoid the .env file, rotate exposed credentials, and avoid passing WiFi passwords directly on the command line.

Risk: Raw API access and disruptive commands can change network state or interrupt service.

Mitigation: Require explicit human approval before raw API calls, restarts, upgrades, port power cycles, blocks, firewall changes, WLAN changes, or other disruptive operations.

Risk: TLS verification is weak for self-signed controller certificates.

Mitigation: Prefer trusted controller certificates where practical and restrict controller access to trusted local networks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/araa47/skills/ez-unifi)
- [Publisher profile](https://clawhub.ai/user/araa47)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands operate through a UniFi controller CLI and may return JSON for supported list operations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
