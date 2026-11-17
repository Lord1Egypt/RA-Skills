## Description:

Transcribe audio using a deployed Cloudflare Worker Whisper endpoint. Use when converting voice/audio files (wav, mp3, m4a, ogg, webm) to text through the custom /transcribe API, including bearer-token auth, plain-text extraction, and quick CLI transcription workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lotfinity](https://clawhub.ai/user/lotfinity)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to send audio files to a deployed Cloudflare Worker Whisper endpoint and receive transcription text or JSON responses. It helps agents prepare bearer-authenticated curl commands, choose audio content types, and run the included helper script for quick transcription workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can send the audio file and bearer token to a URL supplied at runtime.

Mitigation: Use only audio that may be sent to the stated remote service, keep WHISPER_WORKER_TOKEN secret, and avoid the optional URL argument unless the package enforces an allowlisted HTTPS endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lotfinity/skills/cloudflare-whisper-worker)
- [Cloudflare Whisper Worker endpoint](https://lotfi-whisper-worker.medtouradmin.workers.dev/transcribe)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper workflow can return plain transcription text extracted from the worker JSON response.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
