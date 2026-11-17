## Description:

Access ElevenLabs APIs for text-to-speech, speech-to-speech, realtime speech-to-text, voice and model management, and dialogue workflows with direct HTTP calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codedao12](https://clawhub.ai/user/codedao12)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to plan direct ElevenLabs HTTP API workflows for text-to-speech, speech-to-speech, realtime transcription, dialogue generation, and voice/model lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ElevenLabs API keys or single-use tokens could be exposed if placed in client code or logs.

Mitigation: Keep API keys server-side where possible, use scoped or single-use tokens for client contexts, and redact secrets from logs and monitoring.

Risk: Audio or text sent to ElevenLabs endpoints may contain sensitive content.

Mitigation: Send only approved content, avoid logging sensitive audio or text, and use available zero-retention options where eligible.

## Reference(s):

- [Authentication](references/elevenlabs-authentication.md)
- [Text-to-Speech (TTS)](references/elevenlabs-text-to-speech.md)
- [Speech-to-Speech (Voice Changer)](references/elevenlabs-speech-to-speech.md)
- [Speech-to-Text (Realtime)](references/elevenlabs-speech-to-text-realtime.md)
- [Text-to-Dialogue](references/elevenlabs-text-to-dialogue.md)
- [Voices and Models](references/elevenlabs-voices-models.md)
- [Safety and Privacy](references/elevenlabs-safety-and-privacy.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with endpoint checklists and optional code or shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable files are produced by the skill itself.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
