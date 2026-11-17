## Description:

Automatic Speech Recognition (ASR) using Coze API. Use when you need to transcribe audio files to text. Supports Chinese audio transcription via Coze's speech-to-text API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[franklu0819-lang](https://clawhub.ai/user/franklu0819-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to transcribe local MP3, WAV, or OGG audio files through Coze's speech-to-text API, with Chinese as the default language and optional language selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected audio files are uploaded to Coze's API, which can create privacy or consent risk for confidential, regulated, or third-party recordings.

Mitigation: Use only recordings you are authorized to process, avoid confidential or regulated audio unless Coze's data handling terms have been approved, and obtain required consent for third-party recordings.

Risk: The skill requires a COZE_API_KEY to call an external transcription service.

Mitigation: Provide the API key through the environment, avoid embedding it in files or prompts, and rotate it if it is exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/franklu0819-lang/skills/coze-asr)
- [Coze Platform](https://www.coze.cn/)
- [Coze Audio Transcriptions API Endpoint](https://api.coze.cn/v1/audio/transcriptions)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON transcription responses with concise Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq and the COZE_API_KEY environment variable; accepts an audio file path and optional language code.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
