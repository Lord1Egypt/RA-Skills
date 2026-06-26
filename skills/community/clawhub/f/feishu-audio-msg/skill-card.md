## Description: <br>
Sends text-to-speech or existing audio files as playable Feishu audio messages, with optional transcript replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kylinr](https://clawhub.ai/user/Kylinr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to send voice announcements, TTS messages, or existing audio files into Feishu chats while preserving Feishu's playable audio-message UI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses configured Feishu app credentials to upload audio and send messages. <br>
Mitigation: Install only where that credential use is acceptable, and keep Feishu app credentials scoped and protected. <br>
Risk: Audio could be sent to the wrong Feishu chat or user if the receive identifier is incorrect. <br>
Mitigation: Verify the target chat ID or open ID before execution, and test direct-message behavior before relying on it. <br>
Risk: Transcript mode can persist the spoken text as an additional Feishu thread reply. <br>
Mitigation: Use transcript mode only when the text is appropriate to store in chat history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Kylinr/feishu-audio-msg) <br>
- [Feishu file upload API](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu message send API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send generated or supplied audio and optional transcript text through Feishu when executed with configured credentials.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
