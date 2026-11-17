## Description:

Document OCR Agent extracts text, structured entities, and per-page metadata from PDFs, images, and scanned documents through AgentPMT-hosted Google Document AI OCR calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send documents to AgentPMT for OCR, entity extraction, and page-level document metadata in workflows such as receipt capture, invoice parsing, bookkeeping ingestion, and document digitization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted documents may contain sensitive personal, financial, medical, tax, or contractual information and are processed by AgentPMT and Google Document AI.

Mitigation: Submit only documents you are authorized to share, minimize or redact sensitive content where possible, and avoid high-sensitivity documents unless the workflow is approved for that data.

Risk: Setup or related skills may change over time, affecting endpoint, schema, authentication, or payment details.

Mitigation: Use pinned or trusted install sources and refresh live schema or setup instructions before production integration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/document-ocr-agent)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/google-document-ai-ocr)
- [Document OCR Agent schema](schema.md)
- [AgentPMT file-management related skill](https://clawhub.ai/agentpmt/file-management)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON request examples and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides calls that return OCR text, extracted entities, page metadata, warnings, and validation results; extracted text and entities may be truncated by request parameters.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
