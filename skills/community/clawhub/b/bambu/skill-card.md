## Description:

Control Bambu Lab 3D printers via CLI for print management, AMS filament control, temperature, fans, lights, calibration, file management, and live monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g9pedro](https://clawhub.ai/user/g9pedro)

### License/Terms of Use:


## Use Case:

Developers, makers, and printer operators use this skill to check status, manage files and filament, start or control prints, run calibration, and troubleshoot Bambu Lab printers over local LAN access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned globally installed @versatly/bambu CLI package.

Mitigation: Use a pinned and reviewed CLI version or run it in an isolated environment before granting printer access.

Risk: The skill can heat components, move printer axes, delete files, start prints, run calibration, and send raw G-code.

Mitigation: Require explicit user approval before physical-control commands and confirm the printer bed, filament, temperature, and target file are safe for the requested operation.

Risk: The LAN access code and local config file can grant control of the printer.

Mitigation: Protect the LAN access code and ~/.bambu/config.json, and avoid exposing them in prompts, logs, or shared workspaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/g9pedro/skills/bambu)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may read printer status or physically control printer hardware through the local Bambu CLI.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
