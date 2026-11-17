## Description:

Transfers files through Qiniu Kodo using qshell commands for download, upload, and file link exchange.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kadbbz](https://clawhub.ai/user/kadbbz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when an OpenClaw agent must receive or send workspace files through a Qiniu Kodo bucket using qshell.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Qiniu cloud credentials for file transfer.

Mitigation: Use narrowly scoped, rotated credentials from environment variables and review access before installing.

Risk: The skill depends on an external qshell binary.

Mitigation: Download and verify qshell through a trusted Qiniu channel before use.

Risk: The skill can upload files to a third-party storage bucket.

Mitigation: Confirm each file before upload and avoid transferring sensitive data unless the destination bucket and access controls are approved.

## Reference(s):

- [Qiniu Kodo qshell documentation](https://developer.qiniu.com/kodo/1302/qshell)
- [ClawHub skill page](https://clawhub.ai/kadbbz/skills/file-exchange-via-qiniu-kodo)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and file URI messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [File output messages use file_output:// links after successful upload.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
