## Description:

Uploads local files such as images, documents, videos, audio, and archives to an external upload service and returns a directly accessible network URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[piaoleaf](https://clawhub.ai/user/piaoleaf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill when an agent needs to turn a local file into a web-accessible URL for direct reference in webpages, messages, or generated content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local files are uploaded to an external service and may become accessible through a direct URL.

Mitigation: Use the skill only for files approved for external upload, and require user confirmation before uploading sensitive or private content.

Risk: Credential handling is unsafe when JWT tokens are passed through normal shell commands.

Mitigation: Read secrets through a safer local credential flow and avoid exposing tokens in shell history, logs, or process arguments.

Risk: The upload-size limit needs author review and may not match the documented limit.

Mitigation: Fix and verify the enforced upload limit before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/piaoleaf/skills/file-uploader)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Plain text status messages and JSON snippets containing the returned URL, with shell-command guidance for configuration and upload.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The returned URL may directly expose the uploaded file; review files and credentials before upload.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
