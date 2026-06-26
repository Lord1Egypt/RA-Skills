## Description: <br>
Feishu native voice message skill (no ffmpeg needed). Supports multi-language TTS/STT (Chinese, English, etc.) via MiniMax and Edge TTS, with Whisper for receiving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucas260514](https://clawhub.ai/user/lucas260514) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate Feishu-native Ogg/Opus voice messages from text and to support voice transcription workflows with Whisper. It is intended for agents that need multi-language Feishu voice interactions through MiniMax or Edge TTS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text sent for voice generation may include secrets or sensitive conversations. <br>
Mitigation: Avoid sending confidential content through the skill and review Feishu, MiniMax, and Edge TTS data handling requirements before use. <br>
Risk: The skill depends on MiniMax credentials, the mmx CLI, Node.js, and Edge TTS packages. <br>
Mitigation: Install dependencies from trusted sources, protect mmx credentials, and confirm the configured Edge TTS path before execution. <br>
Risk: Temporary MP3 and Ogg audio files are created during conversion. <br>
Mitigation: Run the skill in an environment where temporary audio files are acceptable and clean up generated files according to local retention policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lucas260514/feishu-voice-send) <br>
- [Publisher profile](https://clawhub.ai/user/lucas260514) <br>
- [README.zh-CN.md](artifact/README.zh-CN.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with command examples and generated Ogg/Opus audio file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Feishu-compatible Ogg/Opus audio from text using MiniMax TTS when quota is available and Edge TTS as fallback.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
