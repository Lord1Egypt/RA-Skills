## Description:

Writes application code that generates PDFs with DocSpring through its official 4.x API clients (API v2), covering client setup, typed models for a template's data, the sync API, downloads, batches, combined PDFs, webhook signatures, error handling and tests that catch template changes. Use when the user wants their app to fill a template or generate PDFs with DocSpring ("generate an invoice PDF with DocSpring when an order is paid"), or when a project uses it, such as a docspring, docspring-ts or DocSpring.Client package, DOCSPRING_TOKEN_ID, tpl_ template IDs, sync.api.docspring.com, createSubmission, or 3.x code calling generatePdf. Not for one PDF made from a chat (docspring), building templates (docspring-pdf-templates, docspring-html-templates, docspring-word-templates), signing flows (docspring-signature-requests), or local PDF libraries such as ReportLab or pdf-lib.

This skill is ready for commercial/non-commercial use.

## Publisher:

[docspring](https://clawhub.ai/user/docspring)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to integrate DocSpring's official 4.x API clients (API v2) into applications that fill templates and generate PDFs. It provides language-specific code and guidance for typed template data, downloads, retries, webhooks, and tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submissions may contain customer or invoice data sent to DocSpring.

Mitigation: Confirm the use is authorized, send only fields required by the template, and avoid logging request or response bodies.

Risk: The security review was partial with medium confidence; the TypeScript material was not fully analyzed, and an install command was unpinned.

Mitigation: Review the TypeScript guidance and check the SDK package and install command before adopting it.

## Reference(s):

- [TypeScript and JavaScript reference](references/typescript.md)
- [Python reference](references/python.md)
- [Ruby reference](references/ruby.md)
- [Other languages reference](references/other-languages.md)
- [DocSpring API documentation](https://docspring.com/docs/api/)
- [Migrating to API v2](https://docspring.com/docs/api-guide/migrating-to-api-v2/)
- [Webhook signature verification](https://docspring.com/docs/webhooks/verifying-signatures/)
- [Webhook payloads](https://docspring.com/docs/webhooks/payloads/)
- [Generating PDFs in batches](https://docspring.com/docs/api-guide/generate-pdfs/batch-generate-pdfs/)
- [Combining PDFs](https://docspring.com/docs/api-guide/combine-pdfs/)

## Skill Output:

**Output Type(s):** [Code, JSON schema, Configuration instructions, Shell commands, Guidance]

**Output Format:** [Language-specific code examples and guidance in Markdown, including shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include typed template data models, schema files, API client setup, background job and webhook examples, and tests.]

## Skill Version(s):

1.9.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
