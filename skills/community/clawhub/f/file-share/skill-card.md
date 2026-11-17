## Description:

Transfer files from an OpenClaw workspace to external file-sharing services using curl upload, with support for transfer.whalebone.io.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jakah2551](https://clawhub.ai/user/jakah2551)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to upload workspace files such as logs, reports, media, or generated artifacts to an external sharing service and return a download URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Files uploaded through the skill may become accessible through an external share URL.

Mitigation: Use the skill only for files intentionally meant for external sharing, and avoid sensitive or regulated data unless it is encrypted first.

Risk: The workspace-only validation is not reliable as a security boundary.

Mitigation: Review the file path before upload and do not rely on the validation logic to protect files outside the intended workspace.

## Reference(s):

- [Transfer Service Reference](artifact/references/transfer_service.md)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and returned URL text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uploads a selected workspace file to an external service and returns the service-provided download URL.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
