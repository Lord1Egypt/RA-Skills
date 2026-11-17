## Description:

Unified operating system for controlling embodied intelligent robots with AI agents - the control hub bridging AI agents and physical world.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT

## Use Case:

Developers and robotics engineers use this skill to connect AI agents with simulated or physical robot platforms, generate setup commands and configuration, and draft code for robot perception, planning, safety, and action APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact physical robot operation without enough safety scoping.

Mitigation: Use it first in simulation or a controlled robotics environment, require explicit human confirmation before live-hardware execution, and enforce robot-side workspace, velocity, force, collision, and emergency-stop limits independently.

Risk: The artifact includes unrelated legacy video-generator files that could auto-trigger risky command execution from user-supplied text.

Mitigation: Exclude or ignore the legacy video-generator files for this release and ensure only the Embodied-OS skill file can trigger agent behavior.

Risk: The security review calls for dependency pinning and review before installation.

Mitigation: Pin and inspect Python, npm, ROS, CUDA, and robot-control dependencies before deployment, especially in environments connected to physical hardware.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhenstaff/skills/embodied-os)
- [Project homepage](https://github.com/ZhenRobotics/openclaw-embodied-os)
- [npm package](https://www.npmjs.com/package/openclaw-embodied-os)
- [PyPI package](https://pypi.org/project/openclaw-embodied-os/)
- [v0.1.0 release](https://github.com/ZhenRobotics/openclaw-embodied-os/releases/tag/v0.1.0)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python, YAML, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include package installation commands, API-key configuration guidance, robot-control code snippets, and safety setup examples.]

## Skill Version(s):

0.1.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
