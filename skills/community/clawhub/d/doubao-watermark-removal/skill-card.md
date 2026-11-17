## Description:

Batch remove Doubao (豆包 AI) watermarks from images using OpenCV inpainting for fixed-position watermark areas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dororoliu666](https://clawhub.ai/user/dororoliu666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide batch removal of Doubao or other fixed-position watermarks from image folders they own or have permission to modify.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Watermark removal may be unlawful or inappropriate for images the user does not own or lack permission to modify.

Mitigation: Use the skill only on images the user owns or has explicit permission to edit.

Risk: Using --force can overwrite existing output files.

Mitigation: Use a fresh output directory unless overwriting existing files is intentional.

Risk: Unpinned OpenCV and NumPy dependencies can change behavior across installs.

Mitigation: Install dependencies in a virtual environment and pin package versions before repeatable or production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dororoliu666/skills/doubao-watermark-removal)
- [Publisher profile](https://clawhub.ai/user/dororoliu666)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands and local image file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create cleaned image files in a user-selected output directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
