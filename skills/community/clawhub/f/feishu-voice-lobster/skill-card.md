## Description: <br>
实现飞书语音消息的上传下载、语音转文字及文字转语音，支持与 ElevenLabs 语音服务集成。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godzff](https://clawhub.ai/user/godzff) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers building Feishu bot workflows use this skill to handle voice messages, transcribe user audio with ElevenLabs, synthesize voice replies, and convert audio into Feishu-compatible Ogg/Opus format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu voice recordings may be sent to ElevenLabs for transcription, and the security review notes provider logging may be enabled without clear consent guidance. <br>
Mitigation: Use dedicated API credentials, avoid sensitive or private audio unless consent is clear, and add an explicit approval step or disable provider logging where available before uploading recordings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/godzff/feishu-voice-lobster) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash commands, JavaScript examples, and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials, ELEVENLABS_API_KEY, and FFmpeg; generated audio is converted to Ogg/Opus for Feishu.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
