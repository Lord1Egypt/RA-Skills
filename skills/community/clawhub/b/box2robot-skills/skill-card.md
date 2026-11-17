## Description:

Control Box2Robot robotic arms through a cloud API for servo movement, camera-assisted trajectory recording, dataset download, video generation, and AI training or inference orchestration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boxjod](https://clawhub.ai/user/boxjod)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent operate Box2Robot robotic arms, collect camera-linked trajectory data, prepare datasets and videos, and coordinate training or deployed inference. It is intended for supervised hardware workflows where the operator approves motion, calibration, camera use, deployment, purchases, and third-party task execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Physical robot control can move servos, run calibration, and deploy inference in ways that may injure people or damage objects.

Mitigation: Use only with human supervision, a cleared workspace, trusted device selection, and explicit approval before motion, calibration, or inference deployment.

Risk: The B2R_TOKEN environment variable and ~/.b2r_token file grant device-control access.

Mitigation: Treat the token as a sensitive credential, prefer HTTPS server settings, avoid command-line password exposure, and delete or rotate the token when no longer needed.

Risk: Camera and microphone related operations can capture private information.

Mitigation: Run camera, microphone, recording, and dataset commands only with informed user consent and in an approved environment.

Risk: Purchases and third-party task execution may have financial or operational consequences.

Mitigation: Require explicit human approval before purchases, store execution, or other third-party task actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/boxjod/skills/box2robot-skills)
- [Box2Robot homepage](https://robot.box2ai.com)
- [README.md](README.md)
- [SKILLS.md](SKILLS.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Files]

**Output Format:** [Markdown guidance with CLI examples, configuration notes, and JSON-compatible API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or read local token, dataset, image, and video files during agent-directed Box2Robot workflows.]

## Skill Version(s):

1.0.9 (source: ClawHub release metadata; artifact frontmatter and pyproject.toml list 0.7.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
