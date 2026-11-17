## Description:

Crops long images into Xiaohongshu-friendly 3:4 image slices with command-line, GUI, and mobile collaboration workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[selena001](https://clawhub.ai/user/selena001)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agents use this skill to crop long screenshots, document captures, or design images into Xiaohongshu-ready 1080x1440 image slices. It supports configurable start position, bottom cropping, output format, and output directory through CLI or GUI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invalid or extreme width and height settings, or very large source images, can hang processing or exhaust local resources.

Mitigation: Use positive, reasonable width and height values, avoid very large source images, and review before installing in automated or shared environments.

Risk: The mobile AI-sharing workflow may expose personal, regulated, corporate, or confidential screenshot content.

Mitigation: Do not send sensitive screenshots unless the user is comfortable sharing them with the AI system handling the image.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/selena001/skills/changtu-xiaohongshu-cropper)
- [Skill README](references/README.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; generated PNG or JPG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes local PNG, JPG, JPEG, and WEBP inputs; output dimensions, start Y position, bottom crop height, format, and directory are configurable.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact changelog, released 2026-03-20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
