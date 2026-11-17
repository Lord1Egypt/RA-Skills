## Description:

AUBO Robot provides Python/OpenClaw driver code and guidance for controlling AUBO collaborative robots over RTDE, including joint and Cartesian motion, speed control, status feedback, and digital IO.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qujingyang28](https://clawhub.ai/user/qujingyang28)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics engineers use this skill to integrate AUBO collaborative robots or ARCS simulator instances with an OpenClaw-style Python control workflow for motion, telemetry, speed, and IO operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can drive real robot motion and IO without strong safety scoping or operator controls.

Mitigation: Use only in a controlled robotics environment with a trained operator, emergency stop, cleared workspace, explicit confirmation before motion or IO, and validated speed and workspace limits.

Risk: Status and telemetry methods may be unreliable until they parse real controller responses.

Mitigation: Treat reported status, joint, and TCP pose values as untrusted until verified against the controller or simulator before allowing autonomous actions.

Risk: SDK and robot-controller provenance may be unclear in an installation.

Mitigation: Install only known-safe AUBO/OpenClaw dependencies from trusted sources and review the package before connecting to robot networks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qujingyang28/skills/aubo-robot)
- [AUBO official site](https://www.aubo-robotics.cn/)
- [AUBO developer portal](https://developer.aubo-robotics.cn/)
- [AUBO SDK documentation](https://docs.aubo-robotics.cn/)
- [AUBO download center](https://download.aubo-robotics.cn/)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes robot network configuration values and Python driver interfaces; generated commands or code should be reviewed before use with real hardware.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
