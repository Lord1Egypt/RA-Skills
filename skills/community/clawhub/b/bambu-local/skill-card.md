## Description: <br>
Control Bambu Lab 3D printers locally via MQTT without cloud dependency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tanguyvans](https://clawhub.ai/user/Tanguyvans) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, makers, and developers use this skill to let an agent check status and issue local control commands to supported Bambu Lab printers on a trusted local network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can directly control a physical 3D printer, including stop, temperature, speed, and raw G-code commands. <br>
Mitigation: Use it only on a trusted local network and require explicit user confirmation before non-status commands. <br>
Risk: The printer access code and serial are stored in a local config file. <br>
Mitigation: Keep config.json private, avoid committing it, and restrict filesystem access to trusted users. <br>
Risk: The security summary flags broad device authority and insecure TLS handling for local MQTT control. <br>
Mitigation: Review the skill before use and limit it to trusted LAN environments where the printer endpoint is known. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Tanguyvans/bambu-local) <br>
- [OpenBambuAPI homepage](https://github.com/Doridian/OpenBambuAPI) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples; terminal commands return text status or command confirmations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, paho-mqtt, a local printer IP address, printer serial, and LAN access code.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
