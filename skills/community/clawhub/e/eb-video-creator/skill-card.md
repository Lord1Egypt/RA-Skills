## Description:

Creates videos from scratch using ffmpeg, Python, shell scripts, and user-provided assets for tutorials, slideshows, social media clips, demos, and audiovisual content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emersonbraun](https://clawhub.ai/user/emersonbraun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan and generate code-driven video creation workflows, including ffmpeg commands, Python scripts, platform-specific exports, captions, audio handling, and reusable automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated ffmpeg or shell recipes may overwrite, replace, or remove local media files.

Mitigation: Run commands in a dedicated project folder, review paths and output names before execution, and keep backups of source assets.

Risk: Python video workflows may require dependency installation, including unpinned packages.

Mitigation: Install dependencies in an isolated environment and pin or review package versions before running generated scripts.

Risk: Optional media download workflows can create rights or policy issues when used on unauthorized content.

Mitigation: Use yt-dlp or similar tools only for media you own or are authorized to download and remix.

## Reference(s):

- [FFmpeg Recipes](references/ffmpeg-recipes.md)
- [ClawHub Skill Page](https://clawhub.ai/emersonbraun/skills/eb-video-creator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated ffmpeg commands, Python scripts, asset requirements, platform export settings, and review guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
