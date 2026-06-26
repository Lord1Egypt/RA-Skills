## Description: <br>
ClawVox - ElevenLabs voice studio for OpenClaw. Generate speech, transcribe audio, clone voices, create sound effects, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhishek-official1](https://clawhub.ai/user/abhishek-official1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to call ElevenLabs voice services for text-to-speech, transcription, voice cloning, sound effects, voice isolation, dubbing, and voice library management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected text, audio, and voice samples may be sent to ElevenLabs. <br>
Mitigation: Use the skill only with content approved for ElevenLabs processing and avoid confidential or regulated recordings unless your organization has approved that workflow. <br>
Risk: Voice cloning can create consent and misuse concerns. <br>
Mitigation: Clone voices only with explicit permission from the speaker and keep records of authorization for production use. <br>
Risk: API keys may be exposed in debug or test flows. <br>
Mitigation: Store credentials in protected environment or OpenClaw configuration storage, avoid command-line API keys, and do not run transcription with DEBUG enabled in shared logs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/abhishek-official1/clawvox) <br>
- [ElevenLabs developers](https://elevenlabs.io/developers) <br>
- [ElevenLabs API documentation](https://elevenlabs.io/docs) <br>
- [ElevenLabs voice library](https://elevenlabs.io/voice-library) <br>
- [ElevenLabs pricing](https://elevenlabs.io/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or save audio files through ElevenLabs API calls when invoked by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
