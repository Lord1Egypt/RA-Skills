## Description:

飞书媒体文件发送技能，适用于发送文件、图片、URL图片、视频、音频、语音消息，以及打包压缩后发送。

This skill is ready for commercial/non-commercial use.

## Publisher:

[godzff](https://clawhub.ai/user/godzff)

### License/Terms of Use:


## Use Case:

Agents and users use this skill to send selected local files, images, videos, audio, voice messages, URL images, and compressed archives through Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A selected file or URL image could be sent to the wrong Feishu chat or user.

Mitigation: Verify the destination target before sending any media.

Risk: Private or business-sensitive files could be exposed if the wrong local path or URL is used.

Mitigation: Confirm the exact file path or URL and the sensitivity of the media before sending.

Risk: Voice messages may fail to render as playable Feishu voice messages if the source audio is not Ogg/Opus.

Mitigation: Convert voice audio to Ogg/Opus with ffmpeg and confirm ffprobe can detect duration before sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/godzff/skills/feishu-media)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline message-tool and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Feishu target, message, filePath, media URL, supported format, ffmpeg conversion, and archive packaging guidance.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
