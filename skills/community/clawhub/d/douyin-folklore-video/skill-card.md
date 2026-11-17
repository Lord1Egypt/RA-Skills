## Description:

根据用户提供的中文故事文案，生成配音、竖屏图片、视频片段、字幕和最终视频，并在用户确认后支持上传到抖音。

This skill is ready for commercial/non-commercial use.

## Publisher:

[google696](https://clawhub.ai/user/google696)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and operators use this skill to turn supplied Chinese folklore or eerie-story scripts into short-form Douyin-style videos with voiceover, generated visuals, synchronized subtitles, and an optional publishing step after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary flags account publishing automation and insecure FTP/HTTP media transfer paths as requiring review before installation.

Mitigation: Use only a dedicated low-privilege FTP account and a Douyin account approved for automation; prefer HTTPS object storage, SFTP, or FTPS over FTP/HTTP.

Risk: Story text and generated media are sent to DashScope services and may include user-provided content.

Mitigation: Use non-sensitive story text and require explicit user confirmation before sending content to DashScope or publishing to Douyin.

Risk: The server skill summary says this release is deprecated and should not be installed or used.

Mitigation: Treat the release as historical unless the publisher provides a maintained replacement or a fresh review clears it for use.

## Reference(s):

- [Configuration Reference](references/config.md)
- [ClawHub Skill Page](https://clawhub.ai/google696/skills/douyin-folklore-video)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces voice.wav, generated image files, video segment files, subtitle.srt, and final_video.mp4 when supporting services and credentials are configured.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
