## Description:

Embedded Dev helps agents answer embedded systems development questions across MCU selection, peripheral drivers, embedded C, RTOS, communication protocols, firmware architecture, OTA updates, and hardware/software debugging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzz-pinking](https://clawhub.ai/user/zzz-pinking)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and embedded engineers use this skill to get technical guidance, code examples, shell commands, and troubleshooting steps for microcontroller firmware, RTOS, peripheral interfaces, communication protocols, and debugging workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production-looking firmware examples may include unsafe buffer handling or protocol parsing patterns.

Mitigation: Review and harden generated code with explicit bounds checks, length validation, and target-specific tests before reuse.

Risk: OTA and bootloader guidance may be incomplete for secure firmware update workflows.

Mitigation: Require signed firmware authentication, rollback protection, and device-specific bootloader review before deployment.

Risk: Hardware debugging shell commands can affect connected devices or local captures.

Mitigation: Review commands for the exact board, programmer, and interface, and run them only in an isolated development environment.

## Reference(s):

- [MCU Architectures](references/mcu-architectures.md)
- [Peripheral Drivers](references/peripherals.md)
- [Embedded C](references/embedded-c.md)
- [RTOS](references/rtos.md)
- [Communication Protocols](references/communication-protocols.md)
- [Debugging](references/debugging.md)
- [Firmware Development](references/firmware-dev.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with embedded C and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include example firmware snippets, debugging commands, wiring notes, and troubleshooting checklists.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
