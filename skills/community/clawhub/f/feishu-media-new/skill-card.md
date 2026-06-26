## Description: <br>
飞书媒体文件发送技能。适用于：发送文件、图片、URL图片、视频、音频、语音消息，以及打包压缩后发送。当用户要求在飞书中发送任何类型的媒体文件时激活此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a1024708231](https://clawhub.ai/user/a1024708231) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user asks to send local files, images, URL images, videos, audio, voice messages, or compressed archives through Feishu. It provides message-tool examples and command guidance for Feishu media upload paths, including video and Ogg/Opus voice handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send selected local files, media, or compressed archives to Feishu, which could expose unintended content if the recipient or file set is wrong. <br>
Mitigation: Confirm the exact recipient and file list before sending, and review archive contents before packaging whole folders. <br>
Risk: Video upload guidance uses Feishu app credentials and direct API calls, which can leak secrets if copied into casual prompts or logs. <br>
Mitigation: Keep Feishu app secrets out of chat history and logs, and use a least-privilege Feishu app with only the required messaging and resource permissions. <br>
Risk: Media conversion and upload commands may act on local paths or external URLs supplied by the user. <br>
Mitigation: Review generated shell commands, file paths, and URLs before execution, especially when using ffmpeg, zip, tar, or curl. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/a1024708231/feishu-media-new) <br>
- [Feishu Tenant Access Token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu File Upload API](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu Send Message API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with message-tool examples and bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local file paths, Feishu recipient identifiers, Feishu app credentials, ffmpeg/ffprobe, zip, tar, and curl depending on the requested media type.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
