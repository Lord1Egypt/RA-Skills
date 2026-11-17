## Description:

Feishu Docx helps an agent create and edit Feishu cloud Docx documents through API workflows for document creation, content insertion, batch block updates, Markdown import, and file cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cpjhy](https://clawhub.ai/user/cpjhy)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to automate Feishu Docx creation and editing from agent workflows, including creating documents, appending content, importing Markdown, and managing uploaded files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports bundled live-looking Feishu credentials.

Mitigation: Do not use the bundled credentials; revoke and replace them with credentials stored securely outside the skill.

Risk: The security review reports tenant-specific scripts that upload local content to a fixed Feishu destination without clear user control.

Mitigation: Remove or ignore tenant-specific scripts unless the exact local file and Feishu folder are intended, and verify every remote create, upload, import, or delete operation before execution.

## Reference(s):

- [Feishu Docx API Reference](references/api_reference.md)
- [ClawHub Feishu Docx skill page](https://clawhub.ai/cpjhy/skills/feishu-docx)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python code and shell-oriented execution steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify remote Feishu documents and uploaded files when executed with valid credentials.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
