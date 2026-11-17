## Description:

Extract PDF helps agents process PDFs and images with ComPDF Cloud for structured data extraction, OCR, table extraction, document parsing, conversion, comparison, compression, and PDF page operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[compdf-youna](https://clawhub.ai/user/compdf-youna)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and automation agents use this skill to extract text, tables, OCR results, and structured fields from PDFs or images, and to route related PDF conversion or editing requests through ComPDF Cloud.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises PDF extraction but also enables broader PDF conversion, comparison, compression, page editing, watermark, and related document operations.

Mitigation: Review the selected operation before execution and use editing or transformation actions only when the user explicitly asks for them.

Risk: Documents are uploaded to ComPDF Cloud for processing.

Mitigation: Obtain explicit user confirmation before upload and use only documents the user is allowed to send to ComPDF Cloud; avoid highly sensitive files unless approved.

Risk: The skill may store a ComPDF API public key locally if the user opts in.

Mitigation: Store the key only after explicit user approval and remind users they can delete config/public_key.txt to revoke local storage.

## Reference(s):

- [ComPDF API Overview](https://www.compdf.com/guides/api-reference/v2/overview?utm_source=clawhub&utm_medium=skillhub&utm_campaign=pdf_skill_pdf_extract&ref_platform_id=clawhub_skills)
- [ComPDF API Tool Type Reference](references/tool-list.md)
- [ComPDF API Tool Parameter Details](references/parameters.md)
- [ComPDF API Error Code Reference](references/error-codes.md)
- [ClawHub Skill Page](https://clawhub.ai/compdf-youna/skills/extract-pdf-compdf)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown text with API request parameters, processing status, error suggestions, and expiring download links when processing succeeds.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request an API public key, user consent for external upload, regional base URL selection, optional JSON parameters, and PDF password input for encrypted files.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
