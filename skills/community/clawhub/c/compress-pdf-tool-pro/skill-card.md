## Description:

PDF压缩工具（专业版） guides an agent through uploading PDFs to an external compression API, setting image quality and DPI, polling for completion, and returning download links or reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operations teams, and automation users use this skill to compress single files or batches of PDFs through an API-driven workflow while configuring compression parameters and handling job status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uploads target PDFs to a configured external API service.

Mitigation: Use it only for documents that are approved for that provider, and verify the provider, retention policy, access controls, and report handling before processing confidential, regulated, or client files.

Risk: The skill asks for broad agent tools, including Bash and file write/edit capabilities.

Mitigation: Restrict command execution to explicit commands the user approves and review generated file operations before running them.

Risk: The security scan says the release makes unsupported security and automation claims.

Mitigation: Treat built-in security and audit claims as unverified until deployment-specific controls and logs are reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/compress-pdf-tool-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with Python and YAML snippets, shell commands, and JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include external API requests, PDF upload workflow steps, compression settings, polling status, download links, and batch report structure.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
