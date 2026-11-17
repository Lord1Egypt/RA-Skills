## Description:

A workspace-scoped local file access skill for reading, writing, and listing files in an OpenClaw workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huanz](https://clawhub.ai/user/huanz)

### License/Terms of Use:


## Use Case:

Developers and workspace users use this skill to inspect logs, create Markdown reports, and manage scripts or configuration files inside an OpenClaw workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File write or delete actions could affect workspace files if boundaries or approvals are misconfigured.

Mitigation: Use only in an OpenClaw environment that enforces workspace boundaries, and review write or delete actions before approval.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with file paths and code or shell snippets when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workspace file access should remain within enforced workspace boundaries.]

## Skill Version(s):

1.0.0 (source: release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
