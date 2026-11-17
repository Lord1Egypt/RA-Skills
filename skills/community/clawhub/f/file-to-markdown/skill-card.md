## Description:

Converts documents, spreadsheets, images, structured files, and webpages into clean Markdown optimized for AI processing without authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alaminrifat](https://clawhub.ai/user/alaminrifat)

### License/Terms of Use:


## Use Case:

Developers and AI agents use this skill to convert public URLs or authorized local files into Markdown for RAG ingestion, knowledge base creation, document summarization, dataset extraction, spreadsheet analysis, and automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local files, private URLs, or sensitive documents may be sent to an external conversion service.

Mitigation: Use only files and URLs authorized for processing by markdown.new, and avoid confidential documents, regulated data, credentials, internal-only URLs, private keys, and business-sensitive files unless explicit approval is in place.

Risk: Service processing and retention terms may be unclear for sensitive workflows.

Mitigation: Review the service terms before use in sensitive environments and prefer public or nonsensitive URL conversion when possible.

Risk: Converted Markdown can lose formatting fidelity, especially for complex layouts, spreadsheets, images, or OCR-like extraction.

Mitigation: Validate converted content before using it for RAG ingestion, summarization, analysis, or other downstream automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alaminrifat/skills/file-to-markdown)
- [markdown.new API](https://markdown.new)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with curl, JavaScript, and Python examples; service responses may be plain Markdown or JSON containing Markdown content and metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports remote URL conversion and multipart local file upload; unauthenticated use is documented as 500 requests per day per IP.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
