## Description:

Extracts document structure, text, tables, and figures from PDFs, images, Office documents, and HTML using Azure Content Understanding's prebuilt layout analyzer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zwcih](https://clawhub.ai/user/zwcih)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert documents into Markdown and structured JSON for OCR, layout analysis, table extraction, and downstream document-processing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload document content to Azure Content Understanding.

Mitigation: Use it only for documents intended for Azure processing, and avoid sensitive documents unless that upload is approved for the workflow.

Risk: The skill sends an Azure API key to the configured endpoint and polling URL without validating them.

Mitigation: Use only a trusted HTTPS Azure Content Understanding endpoint, review endpoint configuration before execution, and use a narrowly scoped, rotatable key.

## Reference(s):

- [Azure Content Understanding Layout API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/zwcih/skills/azure-content-layout)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance]

**Output Format:** [Markdown text, structured JSON, stdout text, and optional output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AZURE_CU_ENDPOINT, AZURE_CU_API_KEY, and optionally AZURE_CU_API_VERSION.]

## Skill Version(s):

1.3.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
