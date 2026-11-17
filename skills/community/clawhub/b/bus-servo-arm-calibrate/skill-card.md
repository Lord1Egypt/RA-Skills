## Description:

Calibrate a multi-DOF bus-servo robotic arm (Hiwonder-style, I2C/servo channels, no position readback) when you cannot read servo angles back and must confirm by eye.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sharinchan233](https://clawhub.ai/user/sharinchan233)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, robotics engineers, and operators use this skill to calibrate grasp and placement coordinates for table-top multi-DOF bus-servo arms that lack servo angle readback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Robotic arm calibration can create collision or pinch hazards if attempted in a cluttered workspace.

Mitigation: Keep the robot workspace clear and verify each lift-hold-confirm step visually before continuing.

Risk: In-place edits to calibration scripts or constants can overwrite working arm settings.

Mitigation: Use version control or create a backup before applying calibration parameter changes.

Risk: The arm has no servo angle readback, so incorrect channel direction assumptions can produce unsafe or ineffective movements.

Mitigation: Map each channel and direction first, then tune one slot at a time with human confirmation at a safe lift height.

## Reference(s):

- [bus-servo-arm-calibrate Worked Example](reference.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Human visual confirmation is part of the calibration workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
