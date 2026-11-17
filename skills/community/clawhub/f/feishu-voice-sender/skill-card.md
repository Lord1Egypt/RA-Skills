## Description:

Converts text to Edge TTS speech, converts it to Feishu-compatible OPUS audio, and sends it as a Feishu voice message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwek](https://clawhub.ai/user/wwek)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users can use this skill to turn short text notifications or reminders into spoken Feishu voice messages. It supports reply-style sends to the current chat and targeted sends when a Feishu group ID is provided.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Message text is processed by Edge TTS and sent through Feishu.

Mitigation: Avoid sensitive content unless this external processing is acceptable, and confirm the intended Feishu destination before sending.

Risk: Generated voice files may remain on disk after use.

Mitigation: Clean generated audio files after sending and restrict access to local media directories.

Risk: Runtime behavior depends on external tools and packages.

Mitigation: Use a virtual environment, pinned dependencies, and trusted FFmpeg installation sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwek/skills/feishu-voice-sender)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Plain text status output, shell command usage, and generated OPUS audio media for Feishu.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated voice files may be retained locally until cleaned up; message text is processed by Edge TTS and sent to Feishu.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
