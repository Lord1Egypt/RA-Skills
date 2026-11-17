## Description:

Process video/audio files using FFHub.io cloud FFmpeg API. Use when the user wants to convert, compress, trim, resize, extract audio, generate thumbnails, or perform any FFmpeg operation on media files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gangbo](https://clawhub.ai/user/gangbo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media operators use this skill to prepare FFmpeg commands and run cloud media-processing tasks through FFHub for conversion, compression, trimming, resizing, audio extraction, thumbnail generation, and related media workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs the agent to echo the FFHub API key, which can expose a secret in logs or conversation history.

Mitigation: Check whether FFHUB_API_KEY is set without printing its value, and rotate the key if it has already been exposed.

Risk: Local media may be uploaded to temporary public FFHub storage URLs before processing.

Mitigation: Use the skill only with media the user is comfortable sending to FFHub, and confirm consent before uploading local files.

Risk: The release security verdict is suspicious because of secret-handling and upload-consent concerns.

Mitigation: Review the skill before installation and deployment, and apply the security guidance from ClawHub before use.

## Reference(s):

- [FFHub](https://ffhub.io)
- [FFHub Tasks API](https://api.ffhub.io/v1/tasks)
- [FFHub File Upload API](https://files-api.ffhub.io/api/upload/file)
- [ClawHub Skill Page](https://clawhub.ai/gangbo/skills/ffhub-ffmpeg)
- [ClawHub Publisher Profile](https://clawhub.ai/user/gangbo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include download URLs, file size, processing time, metadata, task status, progress, error details, and suggested fixes.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
