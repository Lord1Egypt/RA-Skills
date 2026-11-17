## Description:

Use when AudioClaw Skills needs to understand a user voice message with AudioClaw ASR, including speech-to-text, model routing for deepthink or pro features, optional timestamps or sentiment, and packaging the result into a ready-to-use AudioClaw user turn payload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kikidouloveme79](https://clawhub.ai/user/kikidouloveme79)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to convert inbound voice messages into transcripts and AudioClaw-ready user turn payloads before the normal dialogue pipeline continues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice recordings are sent to the documented remote ASR service.

Mitigation: Install only when the deployment is allowed to send user audio to the AudioClaw/SenseAudio ASR endpoint and users have appropriate notice or consent.

Risk: The skill depends on unbundled shared runtime code and local credential bootstrap.

Mitigation: Constrain runtime access to trusted shared modules and make credential lookup explicit before production use.

Risk: A default prompt references a prepared cloned voice handoff.

Mitigation: Review or remove the cloned voice handoff unless it is approved for the deployment.

## Reference(s):

- [AudioClaw Voice Intake Reference](artifact/references/openclaw_voice_intake.md)
- [SenseAudio Speech Recognition HTTP API](https://senseaudio.cn/docs/speech_recognition/http_api)
- [AudioClaw Skills Voice Intake on ClawHub](https://clawhub.ai/kikidouloveme79/skills/audioclaw-skills-voice-intake)

## Skill Output:

**Output Type(s):** [text, JSON, configuration]

**Output Format:** [JSON manifest with transcript text and an AudioClaw user turn payload]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include routing metadata, audio metadata, clarification status, raw ASR response, and an optional --out-json file.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
