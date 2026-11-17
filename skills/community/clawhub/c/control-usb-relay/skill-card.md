## Description:

Control USB relay modules with on/off switching, state tracking, and automation support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj-hao](https://clawhub.ai/user/lj-hao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and hardware automation users use this skill to help an agent connect to a USB relay module, switch attached devices on or off, track the last commanded state, and compose relay automation examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running relay tests or generated code can physically switch equipment connected to the relay and may leave the relay on.

Mitigation: Confirm the intended action with the user, test first with low-voltage loads, disconnect real loads during validation, and add physical safety controls before operating connected equipment.

Risk: Setup guidance includes high-impact installation and permission commands.

Mitigation: Review commands before execution, avoid pipe-to-sudo or floating latest installers when possible, prefer pinned and verified packages, and grant serial-port permissions only to appropriate users.

Risk: The reported relay state is the last commanded state and can drift from the physical state after manual override or hardware failure.

Mitigation: Treat in-memory status as advisory, verify hardware state when the connected load matters, and disconnect from the serial port when control is complete.

## Reference(s):

- [Control USB Relay on ClawHub](https://clawhub.ai/lj-hao/skills/control-usb-relay)
- [README](artifact/README.md)
- [Setup - Control USB Relay](artifact/setup.md)
- [USB Relay & Light Sensor Skills - Usage Guide](artifact/USAGE-GUIDE.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent outputs may include commands or Python snippets that control a local serial relay at /dev/ttyUSB1.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
