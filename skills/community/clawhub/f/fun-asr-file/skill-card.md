## Description:

Transcribes local audio files with Alibaba Cloud DashScope FunASR using non-streaming speech recognition optimized for batch file transcription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenggongdu](https://clawhub.ai/user/chenggongdu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to transcribe local audio files such as wav, mp3, m4a, flac, and ogg recordings through Alibaba Cloud DashScope. It is suited to explicit user-requested batch transcription workflows, including downloaded audio that the user is allowed to process.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio content is sent to Alibaba Cloud DashScope for transcription.

Mitigation: Use the skill only for audio the user is allowed to send to DashScope, and ask for explicit confirmation before transcribing sensitive recordings.

Risk: The skill depends on the DashScope Python SDK and optional FFmpeg audio preprocessing.

Mitigation: Install it in a controlled Python environment and pin or review the DashScope SDK version before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenggongdu/skills/fun-asr-file)
- [Publisher profile](https://clawhub.ai/user/chenggongdu)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text transcription output with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY and may require FFmpeg preprocessing to 16 kHz mono wav audio.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
