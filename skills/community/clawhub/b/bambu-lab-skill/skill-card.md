## Description: <br>
Controls and monitors Bambu Lab 3D printers over local-network MQTT for status checks, print progress, temperatures, pause/resume/stop commands, lighting, fan control, and print notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[photonixlaser-ux](https://clawhub.ai/user/photonixlaser-ux) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and 3D-printer owners use this skill to query and control LAN-mode Bambu Lab printers and monitor print progress, completion, and errors from an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill ships with hardcoded printer host, serial number, and access code values that function as printer credentials. <br>
Mitigation: Replace bundled connection values before installation, store credentials securely, and rotate the printer access code if the bundled values were ever real. <br>
Risk: Printer-control commands can pause, resume, stop, or otherwise alter an active physical print job. <br>
Mitigation: Review proposed commands before execution and restrict use to trusted operators on the intended LAN-mode printer. <br>
Risk: Monitoring can run continuously and store printer status locally. <br>
Mitigation: Run monitoring only where local status storage is acceptable and review generated state or notification files for sensitive job details. <br>


## Reference(s): <br>
- [Bambu Lab MQTT API Reference](references/mqtt.md) <br>
- [Bambu Lab Wiki](https://wiki.bambulab.com/en/home) <br>
- [bambu-mqtt Documentation](https://github.com/Doridian/bambu-mqtt) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit live monitoring output, printer status summaries, and command guidance for local MQTT control.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
