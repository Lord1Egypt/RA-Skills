## Description:

Use the baud CLI to diagnose and automate serial, UART, COM-port, USB-to-TTL, and firmware-console workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nitmi](https://clawhub.ai/user/nitmi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to enumerate serial ports, capture boot logs, diagnose communication failures, send bounded device commands, and run guarded YAML workflows against serial hardware.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or invoking an unverified baud-cli package could introduce package-supply-chain risk.

Mitigation: Confirm the package source before installation and pin or independently verify the version when appropriate.

Risk: Serial commands may move, heat, flash, reset, erase, power-switch, or persistently reconfigure connected hardware.

Mitigation: Begin with read-only enumeration and monitoring, verify device identity and state, require positive read-back assertions, and gate hazardous workflow steps with `dangerous: true` and successful prerequisites.

Risk: DTR and RTS line changes can reset or reconfigure some devices.

Mitigation: Keep DTR and RTS disabled unless device documentation requires them, and treat repeated startup banners or disappearing ports as reset or disconnect evidence.

## Reference(s):

- [Serial Hardware Safety and Diagnosis](artifact/references/safety.md)
- [Baud Workflow Authoring and Results](artifact/references/workflows.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and YAML workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference baud JSON or JSONL results, log files, workflow assertions, and exit codes when interpreting serial-device evidence.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
