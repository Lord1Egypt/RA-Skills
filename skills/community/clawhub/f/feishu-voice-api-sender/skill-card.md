## Description: <br>
Sends Feishu voice messages through the official Feishu API by uploading OPUS audio with duration metadata and sending audio messages with the required file key and duration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[54meteor](https://clawhub.ai/user/54meteor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to send existing Ogg Opus audio or generated text-to-speech voice messages to Feishu recipients when the built-in Feishu media sender cannot provide the required duration metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu app credentials are required to obtain tenant access tokens and send messages. <br>
Mitigation: Use a least-privilege Feishu app and provide APP_ID and APP_SECRET through environment variables or a secret manager instead of hardcoding them. <br>
Risk: Voice messages are sent to a caller-provided Feishu open_id. <br>
Mitigation: Verify the recipient open_id before sending and restrict use to intended chats or users. <br>
Risk: Text-to-speech content and audio files may be processed by external services and delivered through Feishu. <br>
Mitigation: Avoid sending secrets, regulated content, or unapproved sensitive data through TTS or voice messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/54meteor/feishu-voice-api-sender) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/54meteor) <br>
- [Feishu Open Platform](https://open.feishu.cn/app) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu file upload API](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu send message API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and Python script usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Feishu API requests that upload audio and send voice messages when invoked with Feishu app credentials, an audio file or TTS text, and a recipient open_id.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
