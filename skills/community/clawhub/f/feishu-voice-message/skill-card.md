## Description: <br>
Generate Feishu voice messages with waveform display from text, converting generated speech to OPUS format for in-chat playback on mobile and desktop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[systiger](https://clawhub.ai/user/systiger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn text into Feishu-compatible voice-message files with waveform playback. It is useful for generating Chinese TTS audio, selecting adult or child voice presets, and preparing OPUS files for Feishu chats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [Feishu Voice Message on ClawHub](https://clawhub.ai/systiger/feishu-voice-message) <br>
- [Feishu File Upload API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/file/create) <br>
- [Edge TTS](https://github.com/rany2/edge-tts) <br>
- [FFmpeg OPUS Encoding](https://trac.ffmpeg.org/wiki/Encode/Opus) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with command examples and generated MP3/OPUS audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces OPUS audio for Feishu voice-message playback; requires local command execution, FFmpeg, and a separate Edge TTS helper path. Avoid confidential text unless the relevant TTS and Feishu services are approved, and confirm the target chat before sending generated audio.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill-info.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
