## Description:

帮助代理将静态图片和动态视频素材合成为FMT肠菌移植科普视频，并生成中文字幕、SRT字幕、TTS旁白、片头片尾和批量工作流输出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, medical-education teams, and agent operators use this skill to assemble FMT educational videos from prepared visual assets, narration text, and subtitles. It supports single-page and batch workflows for generating video files, audio narration, SRT subtitles, and delivery links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated medical-education media may be sent to configured TTS, CDN, or Feishu destinations without sufficient destination review.

Mitigation: Use the skill only where those external services are approved, and require manual confirmation before any upload or send action.

Risk: The fallback workflow may attempt to install system packages such as ffmpeg.

Mitigation: Do not allow package installation unless an administrator has approved the exact package source and command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zmy1006-sudo/skills/fmt-video-production)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with JavaScript examples, Python snippets, bash commands, file paths, and generated media artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces MP4 video files, MP3 narration, SRT subtitle files, intro videos, combined videos, CDN links, and summary reports when the required tools and destinations are available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
