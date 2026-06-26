## Description: <br>
Send and receive Feishu (Lark) voice messages using ElevenLabs text-to-speech and speech-to-text, with guidance for smart voice and text replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DongDongBear](https://clawhub.ai/user/DongDongBear) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to transcribe Feishu voice messages and send generated ElevenLabs audio replies through a Feishu bot. It supports direct voice sending, speech-to-text for received audio, and smart reply workflows that choose voice or text responses based on the incoming message. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send Feishu bot replies on the user's behalf without clear approval, chat limits, or opt-in boundaries. <br>
Mitigation: Require human approval or tightly scoped chats before enabling smart reply behavior, and confirm the target receive_id before sending audio. <br>
Risk: The skill uses Feishu app secrets and an ElevenLabs API key to upload audio, send messages, and transcribe received files. <br>
Mitigation: Store credentials securely, grant only the required Feishu permissions, and avoid exposing secrets in shell history, logs, or shared configuration. <br>
Risk: Voice content and audio files are sent to external services for text-to-speech or speech-to-text processing. <br>
Mitigation: Use the skill only in Feishu spaces where sending bot replies and sending audio to ElevenLabs are acceptable. <br>


## Reference(s): <br>
- [Feishu Voice skill page](https://clawhub.ai/DongDongBear/feishu-voice-elevenlabs) <br>
- [ElevenLabs voice library](https://elevenlabs.io/voice-library) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu file upload API](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [ElevenLabs speech-to-text API](https://api.elevenlabs.io/v1/speech-to-text) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, JSON configuration, plain text transcripts, and Feishu API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ElevenLabs and Feishu credentials, ffmpeg/ffprobe, and the sag CLI for text-to-speech.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
