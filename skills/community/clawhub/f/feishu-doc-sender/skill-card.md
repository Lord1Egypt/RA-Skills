## Description:

Helps agents find Word (.docx) and PDF documents in a workspace and send or prepare them for delivery to Feishu/Lark users and groups with user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timyljob2011-sudo](https://clawhub.ai/user/timyljob2011-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, or developers can ask an agent to locate matching .docx and .pdf files in the workspace, list candidates, and send or prepare them for Feishu/Lark delivery after confirming the selected files and recipient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says document-sending behavior and authority are not clearly implemented or scoped.

Mitigation: Review the installed skill before real Feishu/Lark delivery and confirm exactly which tool or API uploads files.

Risk: Workspace document scanning can surface unintended files.

Mitigation: Constrain the workspace paths that can be scanned and require confirmation of each selected file before sending.

Risk: Documents could be sent to the wrong Feishu/Lark user or group.

Mitigation: Require explicit confirmation of the recipient and destination type before any upload or delivery step.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/timyljob2011-sudo/skills/feishu-doc-sender)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with optional shell commands and file-list text or JSON from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May list matched workspace files, file sizes, and modification times; Feishu/Lark delivery should require explicit confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
