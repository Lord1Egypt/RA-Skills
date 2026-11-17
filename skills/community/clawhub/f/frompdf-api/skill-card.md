## Description:

PDF extraction API for AI agents and LLM pipelines that converts PDFs into semantic AST, markdown, HTML, plain text, or LLM-ready chunks, and also supports semantic diff and readability scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[techtonicllc](https://clawhub.ai/user/techtonicllc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent builders use this skill to extract structured, typed content from PDFs for analysis, RAG ingestion, conversion workflows, semantic comparison, and readability scoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF contents are sent to a third-party service for processing, which can expose confidential, regulated, or legally sensitive documents.

Mitigation: Use only with documents appropriate for frompdf.dev processing, and review the provider's privacy and retention terms before submitting sensitive PDFs.

Risk: Encrypted PDF processing submits the PDF password to the service along with the file.

Mitigation: Avoid encrypted or sensitive PDFs unless the provider's terms and data handling meet the user's requirements.

Risk: The skill requires an API key for a third-party account.

Mitigation: Store FROMPDF_API_KEY in the agent environment or secrets manager, rotate it if exposed, and avoid committing credentials to skill files or logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/techtonicllc/skills/frompdf-api)
- [Publisher profile](https://clawhub.ai/user/techtonicllc)
- [frompdf API homepage](https://api.frompdf.dev)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl examples and JSON, Markdown, HTML, plain text, or chunked API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FROMPDF_API_KEY and uploads selected PDFs to api.frompdf.dev for processing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
