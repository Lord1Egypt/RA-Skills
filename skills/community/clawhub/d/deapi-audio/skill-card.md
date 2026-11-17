## Description:

Text-to-speech, voice cloning, voice design, and audio transcription via deAPI's decentralized GPU network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aleglowa](https://clawhub.ai/user/aleglowa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate spoken audio, clone or design voices, and transcribe audio-only files through deAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload selected text, recordings, voice samples, local files, or URL contents to deAPI.

Mitigation: Use only audio and URLs that the user trusts and has rights to process, especially for voice cloning.

Risk: The skill can expose a stored deAPI API key if config files, logs, or sessions are shared.

Mitigation: Prefer setting DEAPI_API_KEY as an environment variable and avoid sharing logs or sessions that may contain credentials.

## Reference(s):

- [Deapi Audio ClawHub Release](https://clawhub.ai/aleglowa/skills/deapi-audio)
- [deAPI Homepage](https://deapi.ai)
- [Audio API Reference](references/api.md)
- [Voice Reference](references/voices.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scripts can return generated audio URLs, transcription text, model metadata, format, sample rate, and request IDs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
