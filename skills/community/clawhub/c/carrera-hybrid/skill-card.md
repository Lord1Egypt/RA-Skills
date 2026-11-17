## Description:

Control Carrera HYBRID RC cars by Sturmkind via BLE for driving, steering, light control, protocol exploration, Telegram remote control, MITM protocol sniffing, and text-drawing driving paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcel030](https://clawhub.ai/user/marcel030)

### License/Terms of Use:


## Use Case:

Developers, engineers, and hobbyists use this skill to control an authorized Carrera HYBRID RC car from a Linux BLE environment and to understand or document the BLE protocol. It is also useful for controlled protocol analysis and remote-control workflows where physical safety limits are reviewed before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a physical RC car and the security evidence says the script lacks basic safety limits.

Mitigation: Use only with an owned or authorized car in a controlled physical space, set conservative gas and duration values, and add a best-effort stop or finally handler before operation.

Risk: Remote Telegram control can expose physical movement to indirect or unintended commands.

Mitigation: Limit remote access to trusted operators and test commands locally before exposing the car through Telegram or another remote interface.

Risk: MITM protocol sniffing may capture or manipulate BLE traffic outside the intended target.

Mitigation: Perform protocol analysis only on authorized devices in a controlled environment and keep the real car powered off when using the documented fake-peripheral method.

Risk: Unpinned Python dependencies can change behavior over time.

Mitigation: Install dependencies in a virtual environment and pin package versions before operational use.

## Reference(s):

- [Carrera HYBRID BLE Protocol](references/protocol.md)
- [ClawHub skill page](https://clawhub.ai/marcel030/skills/carrera-hybrid)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Linux host with BlueZ, a BLE adapter, Python 3.10+, bleak, and a configured car BLE address.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
