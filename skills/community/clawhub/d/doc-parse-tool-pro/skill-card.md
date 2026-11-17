## Description:

文档解析工具（专业版） guides an agent through PDF, image, and scanned-document parsing, OCR, table extraction, layout analysis, batch processing, and export configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, teams, and automation users use this skill to configure agents for document parsing, OCR, structured extraction, table recognition, layout analysis, batch processing, and export workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes document contents that may contain confidential or sensitive data.

Mitigation: Use it only with documents approved for the agent environment, control the output directory, and review generated text, tables, metadata, logs, and audit records before sharing or retaining them.

Risk: Callbacks or webhooks can transmit parsing status or results outside the local environment.

Mitigation: Disable callbacks unless needed, approve callback destinations before use, and require HTTPS endpoints controlled by the operator.

Risk: Dependency installation and command execution can change the runtime environment.

Mitigation: Install only reviewed dependencies, run with least privilege, and avoid passing untrusted file paths or user input directly into shell commands.

Risk: API keys or document parsing service credentials may be needed for cloud OCR or parsing services.

Mitigation: Provide credentials through environment variables or a managed secret store and remove them from logs, prompts, source files, and generated outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/doc-parse-tool-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with Python, Bash, and YAML snippets; structured parsing results may be exported as JSON, XML, CSV, or HTML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write extracted text, tables, metadata, logs, audit records, and batch output files to a user-selected output directory.]

## Skill Version(s):

1.0.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
