## Description:

Transcribe audio via API Whisper with any compatible local servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nw15d](https://clawhub.ai/user/nw15d)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to transcribe local audio files through an OpenAI-compatible Whisper transcription endpoint, including compatible local Whisper servers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio recordings and the configured API key can be sent to any WHISPER_API_HOST value, including insecure or unintended endpoints.

Mitigation: Use only a trusted HTTPS endpoint or a truly local server, and avoid sending production OpenAI API keys to custom Whisper servers.

Risk: Submitted recordings may contain sensitive data and are uploaded in full to the configured transcription endpoint.

Mitigation: Treat input recordings as sensitive data and review endpoint trust and retention expectations before transcription.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nw15d/skills/any-whisper-api)
- [Publisher profile](https://clawhub.ai/user/nw15d)
- [OpenAI speech-to-text guide](https://platform.openai.com/docs/guides/speech-to-text)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Transcription files written as text or JSON, with shell command guidance for running the transcription script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl plus WHISPER_API_KEY and WHISPER_API_HOST environment configuration.]

## Skill Version(s):

1.3.0 (source: release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
