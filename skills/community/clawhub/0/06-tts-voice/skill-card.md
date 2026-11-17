## Description:

Converts short drama dialogue into expressive text-to-speech audio and returns a generated audio URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ghwyever](https://clawhub.ai/user/ghwyever)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content production teams use this skill to turn short drama dialogue or short-video narration scripts into voiceover audio through a configured TTS provider.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dialogue text and the API key are sent to the configured TTS provider.

Mitigation: Configure API_BASE to a trusted HTTPS endpoint, use a scoped API key with limited quota, and avoid confidential or regulated dialogue unless the provider is approved.

Risk: The configured external TTS provider determines how submitted dialogue is processed.

Mitigation: Review the provider before deployment and prefer a version that documents the external processor and validates the endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ghwyever/skills/06-tts-voice)

## Skill Output:

**Output Type(s):** [audio, text]

**Output Format:** [JSON object containing an audio_url string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires dialogue input plus API_KEY, API_BASE, and MODEL_NAME environment configuration.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
