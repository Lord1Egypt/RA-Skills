## Description: <br>
Embedded Dev helps agents answer embedded systems questions spanning MCU hardware, peripheral drivers, RTOS usage, firmware architecture, communication protocols, debugging, and deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzz-pinking](https://clawhub.ai/user/zzz-pinking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to get embedded systems guidance, code examples, debugging steps, and configuration advice for MCU, firmware, RTOS, peripheral, communication, and low-power design work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect flashing, OpenOCD, GDB, OTA, or hardware commands can damage, erase, or brick a real device. <br>
Mitigation: Review target device names, memory maps, wiring, voltage levels, and recovery options before running commands on hardware. <br>
Risk: Firmware and driver examples may need adaptation for a specific MCU, board revision, SDK, or peripheral configuration. <br>
Mitigation: Validate examples against vendor documentation and bench-test on development hardware before using them in production firmware. <br>
Risk: Bootloader and OTA guidance can make devices unbootable if flash offsets, signatures, CRC checks, or rollback behavior are wrong. <br>
Mitigation: Keep a hardware recovery path, verify flash layout and image validation logic, and test rollback before field deployment. <br>


## Reference(s): <br>
- [Communication Protocols](references/communication-protocols.md) <br>
- [Debugging](references/debugging.md) <br>
- [Embedded C](references/embedded-c.md) <br>
- [Firmware Development](references/firmware-dev.md) <br>
- [MCU Architectures](references/mcu-architectures.md) <br>
- [Peripheral Drivers](references/peripherals.md) <br>
- [RTOS](references/rtos.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with embedded C and shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes hardware wiring considerations, firmware troubleshooting steps, and review-needed commands for target devices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
