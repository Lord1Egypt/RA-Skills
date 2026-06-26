## Description: <br>
Provides embedded development guidance for ARM Cortex-M and RISC-V systems, with focus on Rust embedded-hal drivers, FreeRTOS, async frameworks, peripheral drivers, low-power design, and hardware debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[viewway](https://clawhub.ai/user/viewway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and embedded engineers use this skill as a reference for selecting Cortex-M or RISC-V platforms, building Rust or FreeRTOS firmware, configuring peripherals, debugging hardware, and preparing embedded CI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example flashing or debugging commands could modify firmware or device state on a connected board. <br>
Mitigation: Run commands only on authorized hardware after confirming the chip name, target path, debug probe, and intended firmware image. <br>
Risk: Embedded configuration examples may not match a specific board's memory map, clock tree, peripheral wiring, or safety constraints. <br>
Mitigation: Review examples against the target datasheet, board schematic, linker script, and project safety requirements before applying them. <br>


## Reference(s): <br>
- [ClawHub Embedded ARM Development release](https://clawhub.ai/viewway/embedded-arm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with C, Rust, TOML, YAML, shell command, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance; commands are examples to review against the target chip and authorized hardware before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
