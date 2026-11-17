## Description:

Converts text to speech with Edge TTS and sends the generated voice message to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwek](https://clawhub.ai/user/wwek)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, operators, and developers use this skill to turn short text notifications into Chinese voice messages and send them to Feishu chats. It supports reply-mode delivery to the current chat or targeted delivery when a Feishu chat ID is supplied.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User text is sent to Edge TTS or Microsoft-associated TTS infrastructure before delivery to Feishu.

Mitigation: Use only text approved for that external processing path; avoid secrets, credentials, regulated data, and sensitive internal messages unless the organization has approved the flow.

Risk: Generated audio files are written to /tmp and ~/.openclaw/media/outbound, which may retain message content after use.

Mitigation: Review and clean those locations after use, and apply local retention controls appropriate for the message sensitivity.

Risk: The skill depends on edge-tts, FFmpeg, and the OpenClaw Feishu channel being installed and trusted.

Mitigation: Use pinned dependency versions where possible, install FFmpeg through a trusted package manager, and review the configured OpenClaw destination before sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwek/skills/feishu-tts-edge)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and Python script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates temporary MP3 and OPUS audio files and sends media through the OpenClaw Feishu channel.]

## Skill Version(s):

1.0.1 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
