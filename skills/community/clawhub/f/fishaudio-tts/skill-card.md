## Description:

Converts text to natural-sounding MP3 speech using the FishAudio API, with female, male, and neutral voice options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[izorro](https://clawhub.ai/user/izorro)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to generate local MP3 narration or news audio from supplied text through FishAudio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read FishAudio credentials and proxy settings from a shared TOOLS.md file.

Mitigation: Prefer setting FISH_AUDIO_API_KEY explicitly and avoid storing secrets in a shared TOOLS.md file.

Risk: Input text is sent to the FishAudio cloud API for synthesis.

Mitigation: Do not submit confidential, regulated, or internal text unless it is approved for FishAudio processing.

Risk: Python dependency versions are not pinned in the artifact.

Mitigation: Install dependencies in a pinned virtual environment before use.

## Reference(s):

- [FishAudio website](https://fish.audio/)
- [FishAudio TTS API endpoint](https://api.fish.audio/v1/tts)
- [ClawHub skill page](https://clawhub.ai/izorro/skills/fishaudio-tts)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with command-line examples; runtime output is an MP3 audio file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a FishAudio API key and sends supplied text to the FishAudio cloud API.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
