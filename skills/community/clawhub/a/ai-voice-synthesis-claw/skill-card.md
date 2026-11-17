## Description:

智能配音合成虾 helps agents turn scripts or plain text into AI voiceover audio with selectable voice styles, emotion controls, SSML guidance, and optional post-processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to convert copy, scripts, podcast text, audiobook text, and narration requests into voiceover audio with selected voices, speed, emotion, SSML markup, and optional background music.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance can expose API keys in plaintext logs or transcripts.

Mitigation: Check only whether required environment variables are set, do not print secret values, and rotate any key already exposed.

Risk: Voice synthesis sends provided text to external TTS providers.

Mitigation: Use the skill only with text that is appropriate to send to ElevenLabs or OpenAI, and review provider terms before processing sensitive content.

Risk: Advertised engine coverage and dependency behavior may not match every runtime path.

Mitigation: Verify the available engines against the script before relying on Azure or local fallback behavior, and install pinned dependencies in an isolated environment.

## Reference(s):

- [Audio Processing Guide](references/audio-processing-guide.md)
- [SSML Guide](references/ssml-guide.md)
- [Voice Style Guide](references/voice-style-guide.md)
- [W3C Speech Synthesis Namespace](http://www.w3.org/2001/10/synthesis)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated MP3 or WAV audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call ElevenLabs or OpenAI TTS using API keys; optional post-processing can normalize audio and mix background music.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
