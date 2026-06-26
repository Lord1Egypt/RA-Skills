## Description: <br>
Send voice/audio messages to Feishu (Lark) chats using TTS, using OpenAI TTS when OPENAI_API_KEY is set and macOS say as the fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zihui](https://clawhub.ai/user/zihui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send generated voice messages to Feishu or Lark recipients from an agent workflow. It handles text-to-speech generation, opus transcoding, Feishu file upload, and audio message delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Feishu bot credentials to upload and send audio messages. <br>
Mitigation: Install only for trusted workflows and keep the Feishu app credentials scoped and stored in ~/.openclaw/openclaw.json. <br>
Risk: When OPENAI_API_KEY is set, message text is sent to OpenAI for speech generation. <br>
Mitigation: Unset OPENAI_API_KEY to use the local macOS say fallback for sensitive content. <br>
Risk: Generated audio is sent to the selected Feishu open_id or chat_id. <br>
Mitigation: Review recipient identifiers before execution, especially for group chat delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zihui/feishu-macos-voice) <br>
- [Publisher profile](https://clawhub.ai/user/zihui) <br>
- [OpenAI audio speech API endpoint](https://api.openai.com/v1/audio/speech) <br>
- [Feishu tenant access token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu file upload API endpoint](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu message send API endpoint](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls, audio files] <br>
**Output Format:** [Command-line execution with text inputs, generated opus audio, and Feishu API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS for local say fallback; uses ffmpeg, ffprobe, curl, python3, and Feishu bot credentials.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
