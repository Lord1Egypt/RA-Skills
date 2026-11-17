## Description:

Controls Flipper Zero hardware over USB serial or Bluetooth Low Energy for file, GPIO, screen, input, and radio workflows without an Android device.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elvisexmachina](https://clawhub.ai/user/elvisexmachina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security researchers, and hardware operators use this skill to generate guidance and commands for controlling a physically connected or paired Flipper Zero during device management, screen capture, input automation, and supported radio workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes high-impact device, radio, deletion, and power actions without enforced safety checks.

Mitigation: Review delete, transmit, raw passthrough, GPIO power, reboot, screen capture, and navigation commands explicitly before execution.

Risk: Untrusted text passed into command arguments could trigger unintended Flipper Zero actions.

Mitigation: Avoid passing untrusted text as command input, and inspect generated command arguments before running them.

Risk: Runtime dependencies are installed from package indexes during setup.

Mitigation: Use a dedicated virtual environment and pin dependencies before setup when deploying in controlled environments.

Risk: Radio and external module operations can affect nearby devices or connected hardware.

Mitigation: Use radio transmit and GPIO power actions only with authorization and appropriate hardware precautions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/elvisexmachina/skills/flipper-zero)
- [V3SP3R](https://github.com/elder-plinius/V3SP3R)
- [Flipper Zero Protobuf Definitions](https://github.com/flipperdevices/flipperzero-protobuf)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented command output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local Python scripts that interact with USB serial or BLE hardware.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
