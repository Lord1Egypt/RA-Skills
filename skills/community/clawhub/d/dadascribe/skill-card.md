## Description:

Transcribes, captions, subtitles, and translates audio or video through the DaDaScribe API, supporting URLs, local uploads, diarization, plain transcripts, and SRT outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fablau](https://clawhub.ai/user/fablau)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide agents through DaDaScribe transcription and translation jobs for meetings, interviews, podcasts, videos, and audio or video files. It helps submit sources, poll job status, handle errors, and download transcript or subtitle outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive audio or video may be uploaded to a third-party transcription service.

Mitigation: Confirm explicit user consent before sending private, regulated, business-confidential, or copyrighted media to DaDaScribe.

Risk: The optional GitHub-based package install is unpinned.

Mitigation: Prefer the direct HTTPS API workflow, or pin and inspect the exact package commit in an isolated environment before installation.

Risk: API keys and downloaded outputs may be exposed through logs or uncontrolled storage.

Mitigation: Keep the API key in an environment variable, avoid logging it, and download transcript or subtitle files only to controlled directories.

## Reference(s):

- [DaDaScribe API documentation](https://api.dadascribe.com/docs)
- [DaDaScribe OpenAPI specification](https://api.dadascribe.com/openapi.json)
- [DaDaScribe API base URL](https://api.dadascribe.com/v1)
- [ClawHub skill page](https://clawhub.ai/fablau/skills/dadascribe)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to create transcript and subtitle files downloaded from DaDaScribe output URLs.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
