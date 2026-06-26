## Description: <br>
Use when AudioClaw Skills needs to understand a user voice message with AudioClaw ASR, including speech-to-text, model routing for deepthink or pro features, optional timestamps or sentiment, and packaging the result into a ready-to-use AudioClaw user turn payload. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kikidouloveme79](https://clawhub.ai/user/kikidouloveme79) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn inbound voice messages into transcribed, normalized AudioClaw user turn payloads for downstream dialogue workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected voice messages are uploaded to AudioClaw ASR/SenseAudio for remote transcription. <br>
Mitigation: Use only with audio that is approved for remote processing, and apply the organization's privacy and compliance requirements before broad deployment. <br>
Risk: Sensitive transcript text and audio metadata can appear in command output or saved JSON files. <br>
Mitigation: Limit access to generated manifests and logs, avoid storing unnecessary transcripts, and handle saved JSON as potentially sensitive user data. <br>
Risk: Credential handling depends on local shared helper modules and SENSEAUDIO_API_KEY or workspace credential state. <br>
Mitigation: Review the credential helper path and secret injection process before enabling the skill in regulated or multi-user environments. <br>


## Reference(s): <br>
- [OpenClaw Voice Intake Reference](references/openclaw_voice_intake.md) <br>
- [SenseAudio Speech Recognition HTTP API](https://senseaudio.cn/docs/speech_recognition/http_api) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON manifest with transcript text, routing details, AudioClaw turn payload, and optional saved JSON file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uploads selected audio to AudioClaw ASR/SenseAudio for transcription and may include transcript and audio metadata in command output or saved JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
