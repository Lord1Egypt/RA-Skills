## Description: <br>
Transcribe audio to text using ElevenLabs Scribe, including batch transcription, realtime streaming from URLs, microphone input, and local files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PaulAsjes](https://clawhub.ai/user/PaulAsjes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to convert local files, live streams, or microphone input into text transcripts through ElevenLabs Scribe. It supports optional diarization, language hints, audio-event tagging, partial realtime transcripts, and JSON output with timestamps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio is processed by ElevenLabs under the user's account. <br>
Mitigation: Use the skill only with audio the user intends to send to ElevenLabs, and review account terms and data handling expectations before processing sensitive recordings. <br>
Risk: Microphone mode can capture live audio until it is stopped. <br>
Mitigation: Start microphone mode intentionally, monitor the session, and stop it immediately when transcription is complete. <br>
Risk: ELEVENLABS_API_KEY is required for API access. <br>
Mitigation: Store the API key securely, avoid committing or logging it, and rotate it if exposure is suspected. <br>
Risk: The artifact claims to be an official ElevenLabs skill, but server-resolved publisher evidence identifies the publisher as PaulAsjes. <br>
Mitigation: Verify the publisher and upstream relationship before relying on the official-skill claim for trust decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PaulAsjes/elevenlabs-transcribe) <br>
- [ElevenLabs Speech to Text](https://elevenlabs.io/speech-to-text) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration] <br>
**Output Format:** [Plain text transcripts by default, JSON transcript objects when requested, and realtime transcript lines for streaming modes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ffmpeg, python3, and ELEVENLABS_API_KEY; selected audio is sent to ElevenLabs for transcription.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
