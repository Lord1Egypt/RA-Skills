## Description:

Automatically detects and removes watermarks from images using AI-powered inpainting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fusae](https://clawhub.ai/user/fusae)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run a command-line image cleanup workflow for images they own or are authorized to modify.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Watermark removal can be legally sensitive when applied to images the user does not own or is not authorized to modify.

Mitigation: Use the skill only on owned or authorized images and confirm rights before processing.

Risk: The workflow depends on an unverified external watermark-removal package.

Mitigation: Verify the package publisher, source repository, version, and dependency lockfile before installation.

Risk: Automated detection and inpainting can alter image content unexpectedly.

Mitigation: Run preview mode first and keep backups of original images before writing cleaned outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fusae/skills/fusae-watermark-remover)
- [Publisher profile](https://clawhub.ai/user/fusae)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown with inline bash commands and generated image files from the CLI workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-image and directory inputs, preview mode, detection sensitivity options, mask padding, and OpenCV fallback.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
