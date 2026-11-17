## Description:

Generate vintage comic-book style illustrations from topics, briefings, or meeting notes. Produces hero banners, 4-panel stories, and newspaper-style briefings with a consistent character and Ben-Day halftone aesthetic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adawodu](https://clawhub.ai/user/adawodu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to turn topics, briefings, meeting notes, or uploaded photos into vintage comic-style images for banners, short visual stories, or newspaper-style briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes shell commands for image generation and upload.

Mitigation: Review commands before execution, restrict allowed shell patterns, and require explicit consent before running generation or upload steps.

Risk: Prompts and generated images may be processed externally and permanently hosted.

Mitigation: Use only non-sensitive prompts and images unless external processing and persistent hosting have been approved.

Risk: Prompt text, file paths, and uploaded files may be mishandled without structured validation.

Mitigation: Validate file paths, escape prompt text safely, and allowlist upload endpoints before using the skill with private notes or photos.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/adawodu/skills/comic-brief)
- [Publisher Profile](https://clawhub.ai/user/adawodu)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with shell commands and media URL output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces image-generation prompts, invokes external image processing, uploads generated images to permanent remote hosting, and returns a MEDIA URL.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
