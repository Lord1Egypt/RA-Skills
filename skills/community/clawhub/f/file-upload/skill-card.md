## Description:

Uploads local image, video, and audio files to Flyelep cloud storage through its HTTP API and returns a permanent, publicly accessible direct URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyelepai](https://clawhub.ai/user/flyelepai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an agent needs to convert a selected local media file into a public URL before calling Flyelep image or video workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded files receive permanent public direct URLs.

Mitigation: Upload only selected files that are acceptable for public access, and avoid private, regulated, or sensitive media unless the user has approved that exposure.

Risk: The Flyelep secretKey is required for API access.

Mitigation: Ask for the key at runtime and do not store it in skill files, repositories, logs, or persistent configuration.

Risk: Video and audio uploads are not content-reviewed by the service before storage.

Mitigation: Do not upload unknown-source video or audio, and confirm the source and intended use before creating a public URL.

## Reference(s):

- [ClawHub file-upload Skill Page](https://clawhub.ai/flyelepai/skills/file-upload)
- [Flyelep File Upload API Endpoint](https://www.flyelep.cn/prod-api/poster-design/api/v1/file/upload)
- [Flyelep Open Platform](https://www.flyelep.cn/controlboard)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline HTTP and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns guidance for reading the API response and using data.fullPath as the public media URL.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
