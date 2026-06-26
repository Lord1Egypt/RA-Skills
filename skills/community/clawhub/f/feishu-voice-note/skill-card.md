## Description: <br>
将文本生成语音并转换为飞书支持的 OPUS 音频，然后通过配置的飞书账号发送语音消息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[icesumer-lgtm](https://clawhub.ai/user/icesumer-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn short text replies into Feishu voice-note messages for individual or group chats after TTS generation, OPUS conversion, and recipient selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send Feishu voice messages through a configured account, and the security review notes broad triggers with weak confirmation. <br>
Mitigation: Require explicit confirmation of the recipient and message before sending, and narrow or disable automatic triggers where possible. <br>
Risk: Generated voice content may be processed by the configured TTS provider and delivered through Feishu, which can expose sensitive message content. <br>
Mitigation: Avoid sensitive content unless the TTS provider and Feishu tenant data handling are approved for that use. <br>
Risk: Incorrect Feishu target identifiers or account permissions can send the voice note to the wrong destination or fail unexpectedly. <br>
Mitigation: Validate target Open IDs, use a least-privilege Feishu account, and confirm channel configuration before enabling the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/icesumer-lgtm/feishu-voice-note) <br>
- [OpenClaw documentation](https://openclaw.dev/) <br>
- [FFmpeg documentation](https://ffmpeg.org/documentation.html) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured TTS, ffmpeg, and OpenClaw Feishu channel settings; recipient targets should be selected and confirmed before sending.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
