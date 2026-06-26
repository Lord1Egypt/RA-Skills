## Description: <br>
使用微软 Edge TTS 生成高质量中文语音，默认使用 XiaoxiaoNeural 语音。当用户需要语音回复时自动触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nufeng1999](https://clawhub.ai/user/nufeng1999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add Chinese voice-reply behavior that converts text responses into WAV audio for QQ media delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice-reply behavior may activate too broadly from voice-related prompts. <br>
Mitigation: Use explicit opt-in wording and confirm the user's intent before entering voice or TTS mode. <br>
Risk: Text sent for synthesis may be processed by an external TTS service. <br>
Mitigation: Confirm before sending sensitive text to external TTS services and avoid using the skill for confidential content unless the deployment has approved that service. <br>
Risk: The skill depends on local Python, pip, and edge-tts availability. <br>
Mitigation: Verify the required binaries and package installation path before relying on voice output in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/nufeng1999/chinese-voice-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/nufeng1999) <br>
- [Aliyun PyPI mirror used for edge-tts installation](https://mirrors.aliyun.com/pypi/simple/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and QQ media tags referencing generated WAV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or references WAV audio generated from text through edge-tts when available.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
