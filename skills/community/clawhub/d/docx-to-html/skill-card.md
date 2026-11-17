## Description:

Converts Microsoft Word DOCX documents into semantic HTML for browser viewing, content extraction, and AI processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibekyess](https://clawhub.ai/user/bibekyess)

### License/Terms of Use:

ISC

## Use Case:

Developers and engineers use this skill to convert DOCX files into HTML for web display, indexing, summarization, Q&A, semantic search, and structured content extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Converted HTML can persist the full text, embedded images, and active links from sensitive DOCX files.

Mitigation: Run conversion only on documents approved for that workspace and store generated HTML in controlled locations.

Risk: Generated HTML may be unsanitized and unsafe to embed directly in applications or serve to users.

Mitigation: Treat generated HTML as untrusted, review or sanitize it before browser rendering, embedding, or publication.

Risk: The converter depends on npm packages and DOCX/XML parsing behavior that may need security review.

Mitigation: Audit and update npm dependencies before deployment, and prefer trusted input documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bibekyess/skills/docx-to-html)
- [ClawHub publisher profile](https://clawhub.ai/user/bibekyess)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; conversion produces HTML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, Node.js, and npm dependencies for the mammoth-based converter.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, and artifact/scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
