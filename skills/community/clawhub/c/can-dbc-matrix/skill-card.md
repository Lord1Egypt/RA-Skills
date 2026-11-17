## Description:

Parse and analyze CAN DBC matrix JSON files exported by canmatrix for CAN messages, signals, ECUs, value tables, and decoding workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frankie-zeng](https://clawhub.ai/user/frankie-zeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automotive engineers use this skill to inspect canmatrix-exported CAN database JSON, locate messages and signals, summarize ECU transmitter or receiver relationships, and draft decoding or conversion snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The conversion example depends on the external canmatrix package.

Mitigation: Install canmatrix in a virtual environment and pin or review the package version for sensitive workflows.

Risk: Incorrect bit-numbering assumptions can produce wrong decoded signal values.

Mitigation: Verify Motorola and LSB bit-numbering behavior against the canmatrix export settings before relying on decoded results.

Risk: CAN database outputs may contain local engineering data.

Mitigation: Handle generated summaries and decoded values as local engineering data and review them before sharing.

## Reference(s):

- [Canmatrix JSON Schema Reference](artifact/json-schema.md)
- [ClawHub Skill Page](https://clawhub.ai/frankie-zeng/skills/can-dbc-matrix)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown prose with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local data-handling guidance for CAN database JSON and canmatrix conversion workflows.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
