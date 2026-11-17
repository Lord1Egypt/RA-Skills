## Description:

Provides commands and workflows for Arduino CLI so users can create, compile, and upload Arduino sketches, manage boards, install cores and libraries, and configure Arduino CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[547895019](https://clawhub.ai/user/547895019)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and makers use this skill for Arduino CLI command guidance when setting up projects, managing boards and cores, compiling sketches, uploading firmware, and managing libraries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Arduino CLI upload commands can modify firmware on a connected device if the wrong board, port, or FQBN is selected.

Mitigation: Before running upload commands, confirm the connected board, serial port, and FQBN with `arduino-cli board list`.

Risk: Core and library installation commands can add third-party components to the local Arduino environment.

Mitigation: Review the requested core, library, and additional package index URL before executing install or update commands.

## Reference(s):

- [ESP8266 Arduino Core Package Index](https://arduino.esp8266.com/stable/package_esp8266com_index.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command templates that may install Arduino cores or libraries and upload firmware when executed by the user.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
