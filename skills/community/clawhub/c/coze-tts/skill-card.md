## Description:

Text-to-Speech (TTS) using Coze API. Convert text to natural-sounding speech audio files. Supports multiple voices and output formats (mp3, ogg_opus, wav, pcm).

This skill is ready for commercial/non-commercial use.

## Publisher:

[franklu0819-lang](https://clawhub.ai/user/franklu0819-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send text to Coze's TTS API and save generated speech as MP3, OGG Opus, WAV, or PCM audio files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User text is sent to Coze for text-to-speech processing.

Mitigation: Do not submit secrets, regulated data, or text that should not leave the local environment.

Risk: The Coze API key and submitted text may be visible to local process monitoring while the request runs.

Mitigation: Use a narrowly scoped API key and run the skill only on trusted systems.

Risk: Generated audio files are written to local paths chosen by defaults or user options.

Mitigation: Run from a trusted private directory and provide explicit output paths when file placement matters.

## Reference(s):

- [Coze TTS API reference](artifact/references/coze_tts_api.md)
- [Coze audio speech developer guide](https://www.coze.cn/docs/developer_guides/audio_speech)
- [Coze Platform](https://www.coze.cn/)
- [ClawHub skill page](https://clawhub.ai/franklu0819-lang/skills/coze-tts)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with bash command examples; generated files are audio in mp3, ogg_opus, wav, or pcm format.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq and COZE_API_KEY; ffprobe is optional for duration reporting.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
