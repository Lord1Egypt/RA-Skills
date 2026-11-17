## Description:

Monitor and manage Asus routers running AsusWRT or AsusWRT-Merlin firmware, including status checks, connected clients, presence detection, AiMesh topology, WAN, port, VPN, firmware diagnostics, raw router data dumps, and guarded reboots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rtaylorgraham](https://clawhub.ai/user/rtaylorgraham)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and home-network administrators use this skill to inspect and manage local AsusWRT routers from an agent workflow. It helps troubleshoot internet connectivity, Wi-Fi clients, AiMesh placement, router health, firmware state, VPN status, and controlled reboot operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Router administration commands can expose sensitive network state or affect availability, especially reboot operations.

Mitigation: Review the skill before installation, run it from a dedicated virtual environment, and require explicit confirmation for reboot actions.

Risk: The default example configuration uses local HTTP for high-privilege router access.

Mitigation: Enable HTTPS on the router where stable and set the skill configuration to use HTTPS and the configured secure local port.

Risk: Router credentials stored in config.yaml could be disclosed if committed or shared.

Mitigation: Keep config.yaml out of source control with restrictive permissions and prefer environment variables or a secret store for credentials.

## Reference(s):

- [Asus Router ClawHub release](https://clawhub.ai/rtaylorgraham/skills/asus-router)
- [Home Assistant Asus Router integration](https://github.com/Vaskivskyi/ha-asusrouter)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration guidance]

**Output Format:** [Markdown guidance with CLI commands, human-readable terminal output, and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may require router credentials, local network access, Python dependencies, and the system ping binary.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
