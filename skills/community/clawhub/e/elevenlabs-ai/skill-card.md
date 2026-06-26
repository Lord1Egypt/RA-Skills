## Description: <br>
OpenClaw skill for ElevenLabs APIs: text-to-speech, speech-to-speech, realtime speech-to-text, voices/models, and dialogue workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codedao12](https://clawhub.ai/user/codedao12) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to plan direct HTTPS integrations with ElevenLabs audio APIs for text-to-speech, speech-to-speech, realtime transcription, voice/model lookup, and dialogue workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ElevenLabs API keys or tokens may be exposed if used directly in client contexts or written to logs. <br>
Mitigation: Use scoped API keys or single-use tokens for browser/client calls, redact secrets from logs, and avoid storing credentials in generated examples. <br>
Risk: Submitted audio, generated audio, and transcripts can contain sensitive personal data. <br>
Mitigation: Treat audio and transcript data as sensitive, restrict downstream destinations, and use zero-retention options when they are available for the account and endpoint. <br>


## Reference(s): <br>
- [Authentication](references/elevenlabs-authentication.md) <br>
- [Safety and Privacy](references/elevenlabs-safety-and-privacy.md) <br>
- [Speech-to-Speech](references/elevenlabs-speech-to-speech.md) <br>
- [Speech-to-Text Realtime](references/elevenlabs-speech-to-text-realtime.md) <br>
- [Text-to-Dialogue](references/elevenlabs-text-to-dialogue.md) <br>
- [Text-to-Speech](references/elevenlabs-text-to-speech.md) <br>
- [Voices and Models](references/elevenlabs-voices-models.md) <br>
- [ClawHub release page](https://clawhub.ai/codedao12/elevenlabs-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with endpoint checklists and operational guardrails] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code; guidance is documentation-only.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
