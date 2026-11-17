## Description:

Ai-Thinker-Coder helps agents guide Ai-Thinker IoT module development across WiFi, BLE, LoRa, Radar, NB-IoT, and NearLink modules, with sub-skills organized by chip platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seahi-mo](https://clawhub.ai/user/seahi-mo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as an entry point for Ai-Thinker IoT module workflows, including selecting a chip-specific sub-skill, setting up development tools, building examples, and flashing firmware.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Firmware flashing commands can overwrite firmware on a connected device if the wrong serial port or target board is selected.

Mitigation: Confirm the target Ai-Thinker board, serial port, and readiness to overwrite firmware before running flashing commands.

Risk: External SDK repositories may introduce unexpected build or flashing behavior.

Mitigation: Review external SDK repositories before building or flashing them.

## Reference(s):

- [Ai-Thinker Website](https://www.ai-thinker.com)
- [Ai-Thinker Documentation Center](https://docs.ai-thinker.com)
- [Ai-Thinker Support Forum](https://bbs.ai-thinker.com)
- [Ai-Thinker Open GitHub](https://github.com/Ai-Thinker-Open/)
- [Ai-Thinker WB2 SDK](https://github.com/Ai-Thinker-Open/Ai-Thinker-WB2.git)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes hardware setup, SDK installation, build, and firmware flashing guidance for user-selected Ai-Thinker modules.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
