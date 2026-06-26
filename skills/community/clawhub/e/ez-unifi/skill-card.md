## Description: <br>
Use when asked to manage UniFi network - list/restart/upgrade devices, block/unblock clients, manage WiFi networks, control PoE ports, manage traffic rules, create guest vouchers, or any UniFi controller task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[araa47](https://clawhub.ai/user/araa47) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and network administrators use this skill to inspect and manage UniFi controllers, devices, clients, WLANs, switch ports, firewall objects, traffic rules, and guest vouchers through agent-run commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad administrative control over a UniFi controller, including disruptive network changes. <br>
Mitigation: Use a dedicated least-privileged local account where possible and require explicit approval before commands that restart devices, block clients, change WLANs, alter firewall or traffic rules, power-cycle ports, or use raw API access. <br>
Risk: Controller credentials are stored in a local .env file for command execution. <br>
Mitigation: Protect the .env file, avoid sharing it in logs or repositories, and rotate the dedicated account credentials if exposure is suspected. <br>
Risk: The security guidance calls out TLS verification and raw API access as areas to limit before production use. <br>
Mitigation: Prefer fixing TLS verification for the target controller and restrict or disable raw API usage unless the operator has reviewed the exact request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/araa47/ez-unifi) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/araa47) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-capable command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may read from a local .env file and may return UniFi controller data in table or JSON form.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
