## Description:

Search and manage private, local document collections (PDF, PPTX, DOCX) offline. Use when you need to find information within your private files, not for web research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[docsagent](https://clawhub.ai/user/docsagent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users can use this skill to index and search their own local PDF, PPTX, and DOCX collections, then answer questions from matching local snippets with source citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external npm CLI package as part of installation.

Mitigation: Install only trusted, pinned, or audited versions of @docsagent/docsagent and avoid running npm with elevated privileges.

Risk: Broad local indexing may expose more private documents to local search than intended.

Mitigation: Index only the specific document folders or files needed for the task and review indexed sources with the list command.

## Reference(s):

- [DocsAgent GitHub repository](https://github.com/docsagent/docsagent)
- [DocsAgent ClawHub skill page](https://clawhub.ai/docsagent/skills/docsagent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and source-path citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be grounded in indexed local documents and cite file paths and page numbers when available.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
