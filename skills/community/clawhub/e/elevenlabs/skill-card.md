## Description: <br>
Text-to-speech, sound effects, music generation, voice management, and quota checks via the ElevenLabs API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odrobnik](https://clawhub.ai/user/odrobnik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content teams use this skill to generate speech, sound effects, music, and dialogue with ElevenLabs, manage voices, clone authorized voice samples, and inspect account quota. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an ElevenLabs API key and can also read the key from .env files. <br>
Mitigation: Store ELEVENLABS_API_KEY securely, avoid committing .env files, and rotate the key if it is exposed. <br>
Risk: Voice-cloning samples may contain sensitive biometric or personal audio. <br>
Mitigation: Upload only samples you are authorized to use and keep samples in the configured voiceclone-samples directory or another controlled sample directory. <br>
Risk: Generated audio and quota checks call the ElevenLabs API and may consume account quota or expose prompt content to that service. <br>
Mitigation: Review prompts before execution, monitor quota with the provided quota tool, and avoid sending confidential text unless approved for that service. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/odrobnik/elevenlabs) <br>
- [ElevenLabs Website](https://elevenlabs.io) <br>
- [ElevenLabs Music API Reference](https://elevenlabs.io/docs/api-reference/music/compose) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, audio files, guidance] <br>
**Output Format:** [Markdown guidance and CLI commands; scripts can emit terminal text, JSON, and generated audio files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ELEVENLABS_API_KEY and may consume ElevenLabs account quota.] <br>

## Skill Version(s): <br>
1.3.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
