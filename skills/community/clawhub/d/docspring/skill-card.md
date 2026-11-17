## Description:

Connects to DocSpring, the service that fills PDF and Word templates with data, generates PDFs from HTML templates and collects e-signatures, through its MCP server, CLI or REST API v2, and routes work to the other docspring-* skills. Covers access levels, API tokens, US and EU accounts, templates and their draft and published versions, submissions, test vs live PDFs and credits, IDs, sync waits, errors and rate limits. Use when the user mentions DocSpring or asks to list or fill their templates, make a PDF or Word document from a template, check a submission, review their account or find out why submissions failed, or connect DocSpring, or when a project has a docspring package, tpl_ IDs, DOCSPRING_TOKEN_ID or sync.api.docspring.com. Not for reading, merging or editing local PDF files without DocSpring (use a general PDF skill).

This skill is ready for commercial/non-commercial use.

## Publisher:

[docspring](https://clawhub.ai/user/docspring)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DocSpring account users use this skill to connect an agent to DocSpring and manage templates, submissions, PDF generation, signature requests, account setup, and troubleshooting through MCP, the CLI, or the API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review had medium confidence because coverage was incomplete and some skill text was not fully evaluated.

Mitigation: Review the complete skill and verify critical steps against DocSpring's documentation before using it.

Risk: Submissions can contain personal data.

Mitigation: Read submission data only when needed and keep it out of code, commits, and logs.

## Reference(s):

- [DocSpring ClawHub release page](https://clawhub.ai/docspring/skills/docspring)
- [DocSpring MCP setup](https://docspring.com/docs/mcp/)
- [DocSpring CLI documentation](https://docspring.com/docs/cli/)
- [DocSpring API authentication guide](https://docspring.com/docs/api-guide/authentication/)
- [DocSpring API reference](https://docspring.com/docs/api/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration]

**Output Format:** [Markdown with code and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.9.1 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
