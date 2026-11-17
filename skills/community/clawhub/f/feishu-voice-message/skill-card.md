## Description:

Generate Feishu-compatible OPUS voice-message audio with waveform support from text for playback in Feishu chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[systiger](https://clawhub.ai/user/systiger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn provided text into Feishu-ready OPUS voice-message files with selected Chinese voice presets. It is useful for preparing chat audio that should appear as a playable voice message rather than a generic uploaded audio file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be mistaken for a verified Feishu sender even though server evidence says to treat it as a local audio-file generator.

Mitigation: Confirm the generated OPUS file manually before sending it through Feishu or another chat client.

Risk: The script executes mutable, unpinned external converter code from another local skill path.

Mitigation: Pin or inspect the Edge TTS converter before use and run the skill only in a trusted workspace.

Risk: Generated audio can contain sensitive submitted text and may overwrite predictable output paths.

Mitigation: Use non-sensitive input unless the TTS data flow has been reviewed, and write outputs to a dedicated directory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/systiger/skills/feishu-voice-message)
- [Feishu File Upload API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/file/create)
- [Edge TTS](https://github.com/rany2/edge-tts)
- [FFmpeg OPUS Encoding](https://trac.ffmpeg.org/wiki/Encode/Opus)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with command examples and generated OPUS audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Edge TTS and FFmpeg; generated voice-message files use OPUS audio.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
