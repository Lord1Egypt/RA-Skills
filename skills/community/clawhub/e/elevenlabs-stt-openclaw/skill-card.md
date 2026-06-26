## Description: <br>
Transcribe audio files with ElevenLabs Speech-to-Text (Scribe v2) from the local CLI, with support for diarization, events, JSON output, webhooks, and advanced STT options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xHUNx](https://clawhub.ai/user/xHUNx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to transcribe local audio files, HTTPS audio URLs, or realtime microphone streams with ElevenLabs Speech-to-Text from shell commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio files, microphone streams, transcript text, and webhook metadata may be sent to ElevenLabs or configured webhook endpoints. <br>
Mitigation: Use the skill only with audio and metadata you are authorized to send, avoid sensitive recordings unless consent is clear, and review webhook destinations before use. <br>
Risk: ElevenLabs API keys may be exposed through local process or shell handling. <br>
Mitigation: Run on a single-user machine where possible, avoid sharing shell history or process listings, and rotate the API key if exposure is suspected. <br>
Risk: Live listener modes can continuously capture microphone audio. <br>
Mitigation: Prefer toggle mode or disable live listening when not needed, and confirm the selected microphone device before starting a session. <br>


## Reference(s): <br>
- [ClawHub release: ElevenLabs STT OpenClaw](https://clawhub.ai/xHUNx/elevenlabs-stt-openclaw) <br>
- [Publisher profile: xHUNx](https://clawhub.ai/user/xHUNx) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Plain text transcripts or JSON responses from CLI and realtime streaming commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include diarization, word or character timestamps, audio event tags, webhook metadata, realtime microphone transcripts, and optional TTS playback.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
