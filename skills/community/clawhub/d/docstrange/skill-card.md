## Description:

Document extraction API by Nanonets. Convert PDFs and images to markdown, JSON, or CSV with confidence scoring. Use when you need to OCR documents, extract invoice fields, parse receipts, or convert tables to structured data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shhdwi](https://clawhub.ai/user/shhdwi)

### License/Terms of Use:

UNLICENSED

## Use Case:

Developers and agents use this skill to send selected documents to Nanonets DocStrange for OCR and structured extraction. It is suited for invoices, receipts, contracts, bank statements, forms, scanned document images, and table extraction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected documents are uploaded to Nanonets' external extraction service, which can expose sensitive document contents to a third-party processor.

Mitigation: Use the skill only for documents appropriate for that service, review the provider's retention and compliance terms, and avoid highly sensitive PII until the service posture is approved.

Risk: The skill requires DOCSTRANGE_API_KEY, and exposed credentials could allow unauthorized extraction API use.

Mitigation: Store the key in an environment variable or secret store, avoid committing keys to configuration files, scope permissions where possible, and rotate keys regularly.

Risk: Synchronous extraction is recommended only for documents of five pages or fewer and may time out on larger documents.

Mitigation: Use the async extraction endpoint for larger documents and poll for results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shhdwi/skills/docstrange)
- [DocStrange API Docs](https://docstrange.nanonets.com/docs)
- [DocStrange Dashboard](https://docstrange.nanonets.com/app)
- [DocStrange Homepage](https://docstrange.nanonets.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON, CSV]

**Output Format:** [Markdown guidance with curl commands, configuration snippets, and JSON examples; extraction results may be returned as Markdown, JSON, or CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DOCSTRANGE_API_KEY and sends selected documents to https://extraction-api.nanonets.com.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
