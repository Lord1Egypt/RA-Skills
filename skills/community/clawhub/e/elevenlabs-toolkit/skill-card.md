## Description: <br>
ElevenLabs voice API integration for text-to-speech, sound effects, music generation, speech-to-text, voice isolation, and streaming, requiring ELEVENLABS_API_KEY. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add ElevenLabs voice capabilities to applications, including narration generation, real-time streamed speech, transcription, sound effects, music, and voice isolation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected text and audio to ElevenLabs APIs. <br>
Mitigation: Use it only for content approved for ElevenLabs processing, and provide a clear privacy notice before deployment. <br>
Risk: The included /api/story/chat route can send user messages to Mistral when MISTRAL_API_KEY is configured. <br>
Mitigation: Remove or disable /api/story/chat unless Mistral processing is explicitly approved. <br>
Risk: Exposing the FastAPI router publicly could allow unauthenticated use, uploaded audio abuse, or quota exhaustion. <br>
Mitigation: Add authentication, file-size limits, quota controls, and rate limiting before public deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/elevenlabs-toolkit) <br>
- [ElevenLabs API base URL](https://api.elevenlabs.io/v1) <br>
- [ElevenLabs voices API](https://api.elevenlabs.io/v1/voices) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with Python and shell examples; FastAPI routes return JSON or MP3 audio bytes depending on endpoint.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ELEVENLABS_API_KEY and outbound network access to api.elevenlabs.io.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
