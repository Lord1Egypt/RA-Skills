## Description:

Download videos, images, and audio from YouTube, Twitter, Instagram, Facebook, Vimeo, Tumblr, TikTok, Bilibili, and 1000+ more websites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mstscmsn](https://clawhub.ai/user/mstscmsn)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to extract downloadable media options from supported video and social platforms, select a quality, and receive either a direct link or a locally saved media file. It also guides initial API key setup for the AnyVideos service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted media URLs are sent to the AnyVideos service with the configured API key.

Mitigation: Use the skill only for links that are appropriate to share with the service and keep the API key in the required environment variable.

Risk: The workflow may install ffmpeg and download media files to the local machine.

Mitigation: Require explicit user approval for package installation and file destinations before running shell commands or writing media files.

Risk: Downloaded media can consume significant local storage or exceed chat delivery limits.

Mitigation: Check file size before delivery, use user-approved paths, and prefer private temporary directories with non-overwriting filenames.

Risk: The onboarding text promotes an external signup flow.

Mitigation: Present credential setup neutrally and make clear that use of the external service is required before downloads can proceed.

## Reference(s):

- [AnyVideos homepage](https://anyvideos.yx.lu)
- [ClawHub skill page](https://clawhub.ai/mstscmsn/skills/anyvideos)
- [Publisher profile](https://clawhub.ai/user/mstscmsn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown with tables, inline commands, HTTP examples, and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local media files after user selection and download.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
