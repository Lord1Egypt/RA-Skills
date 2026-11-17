## Description:

Read PDFs and images with EmpirioLabs AI document OCR and return their text as Markdown, preserving tables, formulas, and reading order.

This skill is ready for commercial/non-commercial use.

## Publisher:

[empiriolabs](https://clawhub.ai/user/empiriolabs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing users can extract text and layout from PDFs or images, then print the result or save it as Markdown or JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A redirect weakness may expose the EmpirioLabs API key.

Mitigation: Review redirect handling before installation, use a dedicated key, and rotate it if exposure is suspected.

Risk: The security assessment is partial because some local references could not be resolved.

Mitigation: Treat the assessment as incomplete and review the skill before use.

Risk: Documents submitted for OCR are sent to EmpirioLabs AI for processing.

Mitigation: Submit only documents approved for processing by the service.

## Reference(s):

- [EmpirioLabs AI](https://empiriolabs.ai)
- [EmpirioLabs API documentation](https://docs.empiriolabs.ai)
- [EmpirioLabs MCP setup](https://docs.empiriolabs.ai/mcp)
- [API key setup](https://platform.empiriolabs.ai/dashboard/api-keys)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files]

**Output Format:** [Extracted document text and layout as Markdown, or page results as JSON; can be printed or saved to a file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional page selection and Markdown or HTML table formatting.]

## Skill Version(s):

1.0.0 (source: frontmatter, metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
