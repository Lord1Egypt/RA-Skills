## Description:

Helps agents guide Feishu bot integrations to convert TTS audio from MP3 or WebM into Feishu-compatible Ogg/Opus voice notes with ffmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[17329971](https://clawhub.ai/user/17329971)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers integrating TTS into Feishu, OpenClaw, or custom bot pipelines use this skill to convert generated audio into Feishu voice-note format and plan fallback behavior when conversion fails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ffmpeg may be missing from the target environment, causing conversion to fail.

Mitigation: Confirm ffmpeg is installed and available on PATH before relying on voice-note conversion.

Risk: Temporary audio files can accumulate or expose media if integration code does not clean them up.

Mitigation: Review any integration code added around this guidance for temporary-file cleanup.

Risk: Fallback to MP3 preserves delivery but may render as a file attachment instead of an inline Feishu voice note.

Mitigation: Handle conversion errors explicitly and document the expected attachment fallback behavior.

## Reference(s):

- [Feishu IM message create API](https://open.feishu.cn/document/ukTMukTMukTM/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create_json)
- [ClawHub skill page](https://clawhub.ai/17329971/skills/feishu-voice-note-ffmpeg)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and integration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; does not execute code automatically.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
