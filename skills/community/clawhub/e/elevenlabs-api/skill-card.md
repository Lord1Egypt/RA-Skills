## Description: <br>
ElevenLabs API integration with managed authentication for text-to-speech, voice cloning, sound effects, and audio processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call ElevenLabs through Maton-managed authentication for speech generation, voice management, audio cleanup, transcription, and related audio workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive MATON_API_KEY that can authorize access to connected ElevenLabs accounts. <br>
Mitigation: Keep the key private, pass it through a secure environment variable, and install the skill only if Maton is trusted to proxy the account. <br>
Risk: User-provided text, audio, recordings, and voice samples may be sent to Maton and ElevenLabs for processing. <br>
Mitigation: Avoid confidential recordings, regulated data, private text, and third-party voice samples unless consent and processing approval are clear. <br>
Risk: When multiple ElevenLabs connections exist, requests may target the wrong connected account. <br>
Mitigation: Include the intended Maton-Connection header and confirm the selected connection before making requests. <br>
Risk: Write operations can create, update, or delete voices, projects, history items, and related resources. <br>
Mitigation: Confirm the target resource and intended effect with the user before executing create, update, or delete calls. <br>


## Reference(s): <br>
- [Maton](https://maton.ai) <br>
- [ElevenLabs API Documentation](https://elevenlabs.io/docs/api-reference) <br>
- [ElevenLabs Developer Portal](https://elevenlabs.io/developers) <br>
- [ElevenLabs Models Overview](https://elevenlabs.io/docs/overview/models) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with HTTP endpoint examples and bash, Python, and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and MATON_API_KEY; examples may return JSON metadata, binary audio, streaming audio, or downloaded files when executed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
