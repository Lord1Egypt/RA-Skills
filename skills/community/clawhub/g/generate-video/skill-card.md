## Description:

Generate Video helps an agent call Flyelep's asynchronous video-generation API to create product or creative videos from a text prompt and optional media references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyelepai](https://clawhub.ai/user/flyelepai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to collect video-generation parameters, submit asynchronous Flyelep video jobs, poll for completion, and return the generated video URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User media can be uploaded to Flyelep and exposed through long-lived public URLs.

Mitigation: Use only media suitable for upload to Flyelep; avoid confidential, personal, biometric, customer, or unreleased business media unless separate retention and deletion guarantees are in place.

Risk: The API secret can be exposed if copied into skill files, examples, logs, or persistent configuration.

Mitigation: Request the secret at runtime, place it only in request headers, redact it from logs, and avoid storing it in files or examples.

Risk: Unsafe shell-style JSON examples can break payload encoding or leak data through command history.

Mitigation: Prefer structured HTTP clients or safely serialized JSON payload files, and clean up temporary payload files after use.

Risk: Local file uploads can send the wrong content or exceed service limits.

Mitigation: Ask before each upload, confirm file type and size limits, and reuse a single uploaded URL for the same file within a task.

## Reference(s):

- [ClawHub generate-video release page](https://clawhub.ai/flyelepai/skills/generate-video)
- [Flyelep API key dashboard](https://www.flyelep.cn/controlboard)
- [Flyelep generateVideo endpoint](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/generateVideo)
- [Flyelep queryTaskResult endpoint](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/queryTaskResult)
- [Flyelep file upload endpoint](https://www.flyelep.cn/prod-api/poster-design/api/v1/file/upload)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns an asynchronous task ID first, then a generated video URL after polling succeeds.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
