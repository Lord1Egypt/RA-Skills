## Description:

Feishu native voice message skill (no ffmpeg needed). Supports multi-language TTS/STT (Chinese, English, etc.) via MiniMax and Edge TTS, with Whisper for receiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucas260514](https://clawhub.ai/user/lucas260514)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate Feishu-compatible Ogg/Opus voice audio from text and to support voice-message workflows involving TTS and STT. It is most relevant when replies need to be prepared in Feishu's native voice-message audio format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence says the documentation overstates sending and receiving capabilities.

Mitigation: Verify whether the intended workflow needs only audio generation or actual Feishu send/receive integration before deployment.

Risk: Text or audio may be processed by MiniMax, Edge TTS, Whisper, or related tooling.

Mitigation: Avoid secrets, regulated data, and sensitive conversations unless the provider and dependency trust model is approved.

Risk: The security verdict is suspicious due to capability and third-party processing disclosure gaps.

Mitigation: Review the provider, dependencies, and runtime behavior before installing or enabling the skill for users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lucas260514/skills/feishu-voice-send)
- [Publisher profile](https://clawhub.ai/user/lucas260514)
- [SKILL.md](artifact/SKILL.md)
- [README.zh-CN.md](artifact/README.zh-CN.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with code and shell command examples; runtime script output is an Ogg/Opus audio file path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated audio targets Feishu-compatible Ogg container, Opus codec, 16 kHz sample rate, and mono channel layout.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
