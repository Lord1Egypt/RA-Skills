## Description:

Text-to-Speech and Speech-to-Text using ElevenLabs AI. Use when the user wants to convert text to speech, transcribe voice messages, or work with voice in multiple languages. Supports high-quality AI voices and accurate transcription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amreahmed](https://clawhub.ai/user/amreahmed)

### License/Terms of Use:


## Use Case:

Developers and assistants use this skill to convert text responses into spoken audio, list ElevenLabs voices, and transcribe voice messages into text. It supports command-line and Python-client workflows for voice-enabled assistant interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text and audio selected for processing are sent to the ElevenLabs API.

Mitigation: Use this skill only for content intended for external processing and avoid submitting highly sensitive recordings or confidential text.

Risk: The skill depends on an ElevenLabs API key that may be loaded from the environment or a .env file.

Mitigation: Use a dedicated ElevenLabs API key and avoid storing unrelated secrets in .env files used with this skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amreahmed/skills/elevenlabs-voice)
- [ElevenLabs pricing](https://elevenlabs.io/pricing)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; runtime helpers return JSON-like dictionaries and generated audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ELEVENLABS_API_KEY and sends selected text or audio to the ElevenLabs API.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
