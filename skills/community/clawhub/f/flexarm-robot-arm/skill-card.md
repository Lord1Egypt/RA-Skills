## Description:

FlexArm Robot Arm lets AI agents operate a real smartphone through a robot arm and camera using taps, swipes, OCR, screenshots, and YAML automation scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hamlet0168](https://clawhub.ai/user/hamlet0168)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to control real smartphones with a physical robot arm, camera feedback, OCR, template matching, and reusable YAML automation scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run a powerful persistent Windows robot-control service with administrator setup and weakly documented access controls.

Mitigation: Install only from a trusted source, independently verify downloaded binaries when possible, and run the administrator setup only on a machine where a persistent robot-control service is acceptable.

Risk: Physical phone automation can interact with sensitive apps, screens, or account workflows.

Mitigation: Keep the phone supervised and avoid sensitive apps or screens unless they are necessary for the task.

Risk: Screenshots and YAML automation scripts may contain sensitive local data or executable workflows.

Mitigation: Treat screenshots and YAML scripts as sensitive local data, review scripts before running them, and store outputs only where appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hamlet0168/skills/flexarm-robot-arm)
- [FlexArm release downloads](https://github.com/hamlet0168/flexarm/releases/tag/v2.0.1)
- [FlexArm releases](https://github.com/hamlet0168/flexarm/releases)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP API examples, shell commands, and YAML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a locally running RobotArmServer.exe service on port 7826, calibrated robot hardware, camera visibility, and supervised access to the physical phone.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 2.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
