## Description:

Speech-to-text transcription via Crazyrouter API (OpenAI Whisper).

This skill is ready for commercial/non-commercial use.

## Publisher:

[xujfcn](https://clawhub.ai/user/xujfcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users can use this skill to transcribe audio or video files, optionally provide a language hint, translate speech to English, and save transcript text to a file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio or video recordings and the API key can be sent to Crazyrouter or to the endpoint named by CRAZYROUTER_BASE_URL.

Mitigation: Use only recordings approved for that destination, remove or tightly control CRAZYROUTER_BASE_URL, and use a limited, rotatable API key when available.

Risk: The skill depends on CRAZYROUTER_API_KEY being present in the runtime environment.

Mitigation: Confirm the credential is intentionally configured before use and avoid exposing it in logs, shell history, or shared configuration.

## Reference(s):

- [Crazyrouter](https://crazyrouter.com)
- [Crazyrouter API Base URL](https://crazyrouter.com/v1)
- [ClawHub Skill Page](https://clawhub.ai/xujfcn/skills/crazyrouter-stt)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration instructions]

**Output Format:** [Plain text transcription emitted to stdout or written to a user-specified file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CRAZYROUTER_API_KEY; supports mp3, mp4, mpeg, mpga, m4a, wav, and webm inputs.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
