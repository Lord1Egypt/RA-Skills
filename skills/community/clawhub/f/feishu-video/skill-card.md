## Description: <br>
Helps agents convert audio to OPUS and send Feishu/Lark voice messages, with additional scripts for sending MP4 video messages to users or group chats through the Feishu Open API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangmiok](https://clawhub.ai/user/yangmiok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to prepare media, configure Feishu app credentials, and invoke CLI scripts that upload and send voice or video messages to Feishu users or group chats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu/Lark app credentials can upload and send media externally if exposed or over-permissioned. <br>
Mitigation: Use a least-privilege Feishu/Lark bot, store credentials outside shell history and logs, and rotate secrets if they are exposed. <br>
Risk: Selected audio, video, and generated cover files may be uploaded to Feishu/Lark and delivered to the chosen recipient or group. <br>
Mitigation: Verify the media file path, recipient user ID or chat ID, and intended audience before each send. <br>
Risk: Video and group-chat sending are less prominent than voice-message sending in the public description. <br>
Mitigation: Review the video and chat-targeting behavior before installation and restrict usage to expected media types and destinations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangmiok/feishu-video) <br>
- [OpenClaw integration reference](https://github.com/anthropics/claw) <br>
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu file upload endpoint](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu message send endpoint](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id) <br>
- [Feishu image upload endpoint](https://open.feishu.cn/open-apis/im/v1/images) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, API Calls] <br>
**Output Format:** [Markdown guidance with shell commands and CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create converted OPUS audio files locally and may upload selected audio, video, and cover image files to Feishu/Lark when the scripts are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
