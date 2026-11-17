## Description:

Use when calculating gear ratios, converting RPM between shafts, computing torque output, analyzing drivetrain configurations, or selecting motors for mechanical systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to calculate gear ratios, shaft speed changes, output torque, multi-stage drivetrain behavior, and motor sizing guidance for mechanical systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local shell script with Python for calculations.

Mitigation: Review and scan the artifact before deployment, and require explicit allowed-tools metadata in environments with strict tool declarations.

Risk: Motor-selection and drivetrain outputs are calculation guidance and may not cover all engineering constraints for a physical system.

Mitigation: Validate outputs against project requirements, safety factors, manufacturer data, and qualified engineering review before implementation.

## Reference(s):

- [Gear Skill on ClawHub](https://clawhub.ai/bytesagain3/skills/gear)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown-friendly text and shell command examples with calculation tables and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local calculator output for gear, speed, torque, drivetrain, and motor-selection workflows.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
