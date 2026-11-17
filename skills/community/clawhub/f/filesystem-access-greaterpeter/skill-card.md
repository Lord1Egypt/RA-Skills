## Description:

Provides safe local file read, write, and listing guidance for files inside the OpenClaw workspace by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[greaterpeter](https://clawhub.ai/user/greaterpeter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect, edit, and list files in an OpenClaw workspace, including viewing logs, generating Markdown reports, and saving scripts or configuration files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide read, write, list, or delete-related actions on workspace files.

Mitigation: Keep activity limited to intended workspace-relative paths and review write or delete actions before allowing them.

Risk: The source instructions are written in Chinese, which may not fit every operator workflow.

Mitigation: Install only when Chinese-language skill instructions are acceptable or have been reviewed by someone who can validate them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/greaterpeter/skills/filesystem-access-greaterpeter)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with optional code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local workspace file contents, proposed file changes, or saved workspace files.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
