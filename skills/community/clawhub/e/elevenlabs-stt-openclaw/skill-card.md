## Description:

Transcribes audio files with ElevenLabs Speech-to-Text (Scribe v2) from the local CLI, supporting diarization, events, JSON output, webhooks, and advanced STT options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xhunx](https://clawhub.ai/user/xhunx)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to transcribe local files, hosted audio, or realtime microphone audio with ElevenLabs Speech-to-Text. It is suited for CLI-based transcription workflows that need diarization, audio event tags, JSON output, webhook processing, or realtime transcript text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio and transcript content may be sent to ElevenLabs or a configured webhook endpoint.

Mitigation: Use the skill only for audio you are allowed to send to those services, and review webhook destinations before enabling asynchronous delivery.

Risk: Live-listen and always-on microphone modes can capture private conversations.

Mitigation: Use toggle mode where possible, avoid sensitive environments, and stop the listener when transcription is no longer needed.

Risk: The current scripts can expose the ElevenLabs API key through subprocess arguments.

Mitigation: Run on a single-user machine and use a restricted ElevenLabs API key that can be rotated if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xhunx/skills/elevenlabs-stt-openclaw)
- [ClawHub publisher profile](https://clawhub.ai/user/xhunx)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text transcript or JSON response, with CLI usage guidance in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include word timings, speaker diarization, audio event tags, webhook metadata, or realtime transcript text depending on selected flags.]

## Skill Version(s):

1.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
