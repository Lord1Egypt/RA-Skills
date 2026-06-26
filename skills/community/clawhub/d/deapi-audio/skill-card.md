## Description: <br>
Text-to-speech, voice cloning, voice design, and audio transcription via deAPI's GPU network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aleglowa](https://clawhub.ai/user/aleglowa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to generate speech, clone permitted voices from reference audio, design voices from natural-language descriptions, and transcribe audio-only files through deAPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected text, recordings, voice samples, and generated result URLs are sent to deAPI. <br>
Mitigation: Use the skill only with content that is permitted to upload and not sensitive. <br>
Risk: The skill can store a deAPI API key in config.json if the environment variable is not used. <br>
Mitigation: Prefer DEAPI_API_KEY, protect local config files, and rotate keys if exposure is suspected. <br>
Risk: Voice cloning can be misused without consent from the speaker. <br>
Mitigation: Clone voices only when permission exists for the voice sample and intended generated speech. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aleglowa/deapi-audio) <br>
- [deAPI homepage](https://deapi.ai) <br>
- [Audio API Reference](references/api.md) <br>
- [Voice Reference](references/voices.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON, text] <br>
**Output Format:** [Markdown guidance with bash commands; scripts return JSON containing generated audio URLs, transcription text, request IDs, and model metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and DEAPI_API_KEY; result URLs expire in 24 hours.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; source frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
