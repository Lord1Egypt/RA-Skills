## Description:

Document to Markdown converter - convert DOCX, PPTX, Excel files to Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanis90](https://clawhub.ai/user/tanis90)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to extract content from Word, PowerPoint, and Excel files and return the content as Markdown for reading, summarization, or analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents are uploaded to MinerU's cloud service for processing.

Mitigation: Use the skill only for documents appropriate for external cloud processing, and avoid confidential or regulated content unless the provider and data handling terms are approved.

Risk: The required mineru-open-api CLI is installed from external package sources.

Mitigation: Install from trusted sources, prefer pinned or reviewed versions, and verify the CLI before using it in sensitive environments.

Risk: Larger-file extraction may require authentication with the provider.

Mitigation: Avoid authenticated extraction unless the user trusts the provider and understands the account-level implications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tanis90/skills/document-to-markdown)
- [MinerU](https://mineru.net)
- [MinerU CLI download](https://mineru.net/ecosystem?tab=cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands when CLI execution is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes DOCX, PPTX, XLS, and XLSX inputs through the MinerU Open API; flash extraction is documented for files up to 10MB or 20 pages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
