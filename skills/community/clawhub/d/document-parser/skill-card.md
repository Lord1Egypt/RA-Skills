## Description:

Extract structured data from PDFs, images, and Word files with layout analysis, table recognition, OCR, seal detection, and directory extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ankylala](https://clawhub.ai/user/ankylala)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to parse PDFs, images, and Word documents into structured JSON or Markdown, including document elements such as paragraphs, tables, images, seals, formulas, and tables of contents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected documents and optional API credentials may be sent to a configured remote parsing service.

Mitigation: Use a trusted HTTPS endpoint, understand the operator's retention practices, and use revocable credentials.

Risk: The default endpoint is plaintext HTTP, which is inappropriate for sensitive documents or API keys.

Mitigation: Override the base URL with a trusted HTTPS endpoint before processing sensitive content.

Risk: Runtime dependencies are specified with lower bounds rather than pinned versions.

Mitigation: Pin or lock dependencies before deploying in a controlled environment.

## Reference(s):

- [Document Parser ClawHub Skill Page](https://clawhub.ai/ankylala/skills/document-parser)

## Skill Output:

**Output Type(s):** [text, markdown, files]

**Output Format:** [Structured JSON and Markdown, typically saved as a parsed output file or returned as CLI status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include page metadata, document elements, request identifiers, elapsed time, and parser error codes.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
