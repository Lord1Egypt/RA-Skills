## Description: <br>
Feishu Voice converts text into speech, converts the audio to Feishu-compatible opus format, uploads it, and sends it as a playable Feishu voice message. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[franklu0819-lang](https://clawhub.ai/user/franklu0819-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send generated voice messages into Feishu chats from agent workflows. It is suited for automating text-to-speech notification flows that rely on Feishu bot credentials and a configured Coze TTS dependency. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provided text is processed by the configured TTS dependency and the resulting audio is uploaded and sent through Feishu. <br>
Mitigation: Use this skill only for approved data flows, and avoid sending secrets, regulated data, or sensitive business content unless that use is authorized. <br>
Risk: Feishu bot credentials authorize message upload and send actions. <br>
Mitigation: Use least-privilege Feishu bot credentials and keep the coze-tts dependency from a trusted installation. <br>


## Reference(s): <br>
- [Feishu Voice API Reference](references/feishu_voice_api.md) <br>
- [Feishu Message Create API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create) <br>
- [ClawHub Feishu Voice Listing](https://clawhub.ai/franklu0819-lang/feishu-voice) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Text with shell command invocations and configuration requirements] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When executed, the bundled script may create temporary audio files and send audio messages through Feishu.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
