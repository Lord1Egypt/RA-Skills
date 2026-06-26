## Description: <br>
飞书媒体文件发送技能。适用于：发送文件、图片、URL图片、视频、音频、语音消息，以及打包压缩后发送。当用户要求在飞书中发送任何类型的媒体文件时激活此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godzff](https://clawhub.ai/user/godzff) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill to send local files, images, URL images, videos, audio files, voice messages, and compressed archives through Feishu. It is intended for workflows where the agent must share media with a specified Feishu chat or user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can send local files, URL media, or archive contents to Feishu recipients, which may expose confidential documents, personal data, credentials, or unintended attachments. <br>
Mitigation: Before each send, confirm the exact recipient, local file path or URL, and archive contents. <br>
Risk: Voice-message workflows depend on Ogg/Opus conversion and duration detection with ffmpeg and ffprobe. <br>
Mitigation: Verify the converted audio format and duration before sending when a playable Feishu voice message is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/godzff/feishu-media) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent to call the Feishu message tool with target, filePath, media URL, and optional message fields.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
