## Description:

Operate and troubleshoot BambuLab printers with bambu-cli by producing safe commands for setup, monitoring, printing, files, camera, G-code, AMS, calibration, motion, fans, light, configuration, and diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobiasbischoff](https://clawhub.ai/user/tobiasbischoff)

### License/Terms of Use:


## Use Case:

Developers, operators, and printer owners use this skill to translate BambuLab printer tasks into bambu-cli commands for monitoring, configuration, printing, file handling, camera snapshots, calibration, diagnostics, and controlled hardware actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-driven printer control can affect physical hardware through print control, file deletion, calibration, reboot, and raw G-code commands.

Mitigation: Require explicit user confirmation for destructive actions, prefer dry-run previews when supported, and use force or confirmation flags only after the user explicitly agrees.

Risk: Raw G-code sent with validation bypassed can create hardware risk.

Mitigation: Prefer validated G-code commands and use `gcode send --no-check` only when the user explicitly understands and accepts the risk.

Risk: Printer access codes can be exposed if passed directly as command-line flags.

Mitigation: Use access-code files or stdin for credentials, and avoid combining access-code stdin with G-code stdin.

## Reference(s):

- [bambu-cli command reference](artifact/references/commands.md)
- [ClawHub skill page](https://clawhub.ai/tobiasbischoff/skills/bambu-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON or plain key=value output flags when structured command output is requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
