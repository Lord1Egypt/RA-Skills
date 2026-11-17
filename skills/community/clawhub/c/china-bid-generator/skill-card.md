## Description:

China Bid Generator helps agents draft Chinese tender and bid documents, including tender notices, bid proposals, technical plans, and commercial quotations for sectors such as government procurement, engineering, IT, medical equipment, and education.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate China-market tender and bid document drafts from project information, user-provided materials, and selected industry templates. Generated documents should be manually reviewed for accuracy, compliance, and confidentiality before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated bid and tender documents may contain incorrect, incomplete, or non-compliant content.

Mitigation: Manually review every generated document for legal, procurement, pricing, and factual accuracy before submission or external distribution.

Risk: Project details, pricing, bid strategy, government requirements, or private source files may be exposed if supplied to web search or external tools.

Mitigation: Use isolated environments and only provide confidential materials to external services when that disclosure is explicitly approved.

Risk: The bundled code may produce a basic Word document rather than every advertised document type or workflow.

Mitigation: Validate generated `.docx` or PDF files against the intended bid package requirements and add missing sections manually.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobewin/skills/china-bid-generator)
- [Publisher profile](https://clawhub.ai/user/tobewin)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python examples and generated Word or PDF document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; artifact metadata lists python-docx and fpdf2 dependencies.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
