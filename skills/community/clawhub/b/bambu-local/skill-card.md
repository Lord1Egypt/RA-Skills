## Description:

Control Bambu Lab 3D printers locally via MQTT (no cloud). Supports A1, A1 Mini, P1P, P1S, X1C.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanguyvans](https://clawhub.ai/user/tanguyvans)

### License/Terms of Use:


## Use Case:

Developers, engineers, and printer operators use this skill to let an agent check status and send local control commands to supported Bambu Lab printers without relying on cloud services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send high-impact physical printer commands, including raw G-code, print stop, speed, and temperature changes.

Mitigation: Review commands before execution and add confirmations or command restrictions before routine use.

Risk: The skill disables TLS certificate verification for the local MQTT connection.

Mitigation: Use only on a trusted local network and prefer certificate pinning before routine use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tanguyvans/skills/bambu-local)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and local printer configuration with printer IP, LAN access code, serial number, and printer name.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
