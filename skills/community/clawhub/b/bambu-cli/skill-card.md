## Description: <br>
Operate and troubleshoot BambuLab printers with bambu-cli, including status checks, print control, file management, camera snapshots, G-code, AMS, calibration, motion, fans, light, configuration, and diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobiasbischoff](https://clawhub.ai/user/tobiasbischoff) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and support engineers use this skill to translate BambuLab printer tasks into safe bambu-cli commands for setup, monitoring, printing, file transfer, camera snapshots, maintenance, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Printer-control commands can stop jobs, delete files, send G-code, calibrate hardware, move axes, change temperatures, or reboot a printer. <br>
Mitigation: Review proposed commands before execution and require explicit confirmation for destructive or hardware-affecting actions. <br>
Risk: Printer access codes could be exposed if placed directly in command flags or logs. <br>
Mitigation: Use access-code files or stdin, protect those files, and avoid passing access codes as command-line arguments. <br>
Risk: Incorrect target selection could affect the wrong printer profile or device. <br>
Mitigation: Confirm the intended printer profile, IP address, and serial number before running control commands. <br>


## Reference(s): <br>
- [bambu-cli command reference](references/commands.md) <br>
- [ClawHub skill page](https://clawhub.ai/tobiasbischoff/bambu-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON or plain-output flags when structured command output is useful.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
