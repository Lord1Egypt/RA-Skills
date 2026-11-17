## Description:

Resize video outputs for social, ecommerce, ads, and platform uploads without stretching the subject or breaking compatibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, ecommerce teams, and agents use this skill to plan platform-ready video resize variants, select crop, pad, or scale strategies, and document framing and compatibility tradeoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A proposed resize can crop faces, products, subtitles, or other priority visual areas.

Mitigation: Confirm the priority visual area and review crop, pad, or scale tradeoffs before producing final outputs.

Risk: A video-processing command can target the wrong input, output path, dimensions, or overwrite behavior.

Mitigation: Review proposed commands before execution and verify the source file, destination path, dimensions, aspect-ratio strategy, and overwrite flags.

## Reference(s):

- [Video Resizer Output Template](references/output-template.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with optional video-processing commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes resize strategy, output dimensions, framing notes, compatibility notes, and optional additional recommended sizes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
