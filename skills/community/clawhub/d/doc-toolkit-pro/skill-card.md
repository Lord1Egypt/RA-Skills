## Description:

文档工具箱专业版 helps agents automate enterprise DOCX workflows including batch generation, template management, mail merge, version comparison, watermarking, encryption, and multi-format export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Document teams, HR, sales, finance, legal, and developers use this skill to generate, compare, protect, and export structured DOCX documents from templates and tabular data. It is suited for controlled document automation workflows rather than tasks requiring open-ended creative judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive business documents such as contracts, HR records, financial reports, and customer data.

Mitigation: Confirm where document data is processed, limit input folders and output or version directories, and avoid running it on sensitive corpora until data handling is approved.

Risk: Batch document generation and shell-command-backed conversions can affect many files quickly.

Mitigation: Require explicit approval before batch runs, test on sample documents first, and constrain allowed conversion commands and output locations.

Risk: Callback or protocol endpoint integrations may expose document automation outside the local workflow.

Mitigation: Disable endpoint integrations unless required, and review authentication, callback destinations, and transport security before enabling them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/doc-toolkit-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command examples and structured JSON-style result descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce document workflow instructions, template and data configuration examples, conversion commands, and operational guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
