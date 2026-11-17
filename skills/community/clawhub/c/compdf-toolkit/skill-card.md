## Description:

All-in-one ComPDF workflow for document conversion, OCR, data extraction, PDF editing, protection, compression, and watermarking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[compdf-youna](https://clawhub.ai/user/compdf-youna)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to plan ComPDF Server API requests for document conversion, OCR, extraction, PDF editing, protection, compression, watermarking, and related PDF workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected documents and PDF passwords may be sent to ComPDF for processing.

Mitigation: Confirm the affected files and destination before upload, and avoid using the skill for documents whose sensitivity or policy restrictions do not allow ComPDF processing.

Risk: The skill uses a skill-local api_key file for ComPDF credentials.

Mitigation: Keep the file private, exclude it from source control and archives, and rotate the ComPDF key if exposure is suspected.

Risk: PDF decryption, protection changes, watermark removal, deletion, or overwrite-style workflows can alter document access or content.

Mitigation: Require explicit confirmation before operations that overwrite, delete, decrypt, remove watermarks, or apply permanent protection, and preserve originals unless replacement is requested.

Risk: AI parsing and extraction can expose sensitive fields from confidential documents.

Mitigation: Review document sensitivity before extraction and restrict use to workflows where the extracted fields may be processed by ComPDF.

## Reference(s):

- [ComPDF Endpoint Index](references/endpoint-index.md)
- [Official ComPDF V2 API Reference Snapshot](references/official-api-reference.md)
- [ComPDF Conversion API Catalog](https://www.compdf.com/guides/api-reference/v2/api-overview)
- [ComPDF PDF API Catalog](https://www.compdf.com/guides/api-reference/v2/api-overview-pdf)
- [ComPDF Authentication](https://www.compdf.com/guides/api-reference/v2/authentication)
- [ComPDF Request Workflow](https://www.compdf.com/guides/api-reference/v2/request-workflow)
- [ComPDF AI Overview](https://www.compdf.com/guides/api-reference/v2/ai/overview)
- [ComPDF Portal](https://www.compdf.com/compdf-portal/signin?utm_source=clawhub&utm_medium=referral&utm_campaign=compdf_skills_repo_en&ref_platform_id=clawhub_compdfkit_skills_en)
- [ClawHub Skill Page](https://clawhub.ai/compdf-youna/skills/compdf-toolkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with endpoint details, request fields, response fields, and follow-up steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request plans, credential setup guidance, polling or download steps, and safety confirmations before uploads or destructive PDF operations.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
