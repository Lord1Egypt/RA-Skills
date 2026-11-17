## Description:

Feishu Docs is an agent skill for creating, reading, updating, deleting, converting, searching, and sharing Feishu Docx cloud documents through the Feishu Open Platform API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binbin](https://clawhub.ai/user/binbin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let an agent manage Feishu Docx documents, including document creation, content updates, Markdown or HTML conversion, search, export, and permission management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete, replace, or share Feishu cloud documents.

Mitigation: Require human confirmation before delete, full replace, or permission-changing commands, and use a least-privileged Feishu app.

Risk: App secrets can be supplied through command-line arguments.

Mitigation: Prefer protected environment variables or secret-manager injection and avoid passing secrets with --app-secret.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/binbin/skills/feishu-docs-1-1-1)
- [Feishu Open Platform Docx API Overview](https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/overview)
- [Feishu Open Platform App Console](https://open.feishu.cn/app)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify Feishu cloud documents and permissions through authenticated API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact package.json reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
