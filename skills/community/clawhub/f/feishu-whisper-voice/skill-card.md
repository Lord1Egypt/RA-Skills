## Description:

Uses Faster-Whisper for speech recognition and Feishu text-to-speech tools to help an agent process voice messages and produce spoken replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[15071664](https://clawhub.ai/user/15071664)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Feishu bot operators use this skill to add voice-message transcription, AI response generation, and text-to-speech replies to Feishu-based agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled scripts include unsafe defaults that may read stale local audio resources or write transcripts to a shared temporary path.

Mitigation: Run the skill in an isolated environment, remove hard-coded temporary paths, and explicitly manage deletion and access controls for audio files and transcripts.

Risk: Some helper scripts install packages at runtime or modify shell startup files.

Mitigation: Review scripts before execution, install dependencies through a controlled environment, and prevent installers from changing shell startup files.

## Reference(s):

- [Faster-Whisper GitHub](https://github.com/guillaumekln/faster-whisper)
- [Hugging Face Faster-Whisper Base Model](https://huggingface.co/systran/faster-whisper-base)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [ClawHub Skill Page](https://clawhub.ai/15071664/skills/feishu-whisper-voice)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents toward local speech-to-text transcripts and text-to-speech reply handling; helper scripts may emit console text or local transcript files.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
