## Description: <br>
Feishu Voice Sender creates TTS voice messages for Feishu/Lark and can optionally transcribe explicitly provided OGG/Opus audio with ASR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunxq1017-hash](https://clawhub.ai/user/sunxq1017-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when a user explicitly asks the agent to send a Feishu/Lark voice message or to recognize a selected OGG/Opus audio file. It converts user-provided text to speech through Volcengine, sends the resulting audio through Feishu/Lark, and returns ASR text when the optional recognition path is invoked. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided text and selected audio are processed by external Volcengine and Feishu/Lark services. <br>
Mitigation: Use the skill only for intended voice-message workflows, avoid sensitive content unless external processing is acceptable, and disclose the external data flow to operators. <br>
Risk: Feishu and Volcengine credentials can send messages or access speech services if over-privileged or exposed. <br>
Mitigation: Store credentials in environment variables, grant least-privileged access, rotate secrets regularly, and avoid sharing logs that may reveal configuration. <br>
Risk: ASR could process an unintended local audio file if invoked with the wrong path. <br>
Mitigation: Invoke ASR only on user-selected .ogg files and keep the documented file-type and explicit-invocation checks enabled. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sunxq1017-hash/feishu-voice-sender-tts) <br>
- [Volcengine Console](https://console.volcengine.com/) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>
- [Volcengine ASR Flash Recognize API](https://openspeech.bytedance.com/api/v3/auc/bigmodel/recognize/flash) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Configuration, Shell commands] <br>
**Output Format:** [Python function calls that send Feishu/Lark voice messages and return boolean status or ASR text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu and Volcengine credentials; TTS text is capped at 300 characters; ASR accepts explicitly selected .ogg audio files.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata and SKILL.md changelog, released 2026-03-24) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
