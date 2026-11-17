## Description:

Compare two images or PDFs for visual similarity via the PDFAPIHub cloud API. Documents are uploaded to pdfapihub.com for comparison using feature matching, SSIM, or perceptual hashing. Requires a CLIENT-API-KEY header.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rishabhdugar](https://clawhub.ai/user/rishabhdugar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to compare images or PDFs for duplicate detection, template consistency checks, QA regressions, fraud review, and document version comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Compared documents, document URLs, and the PDFAPIHub API key are sent to PDFAPIHub for cloud processing.

Mitigation: Use only when sending the documents and credential to PDFAPIHub is acceptable; review the provider's privacy and retention terms before processing confidential files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rishabhdugar/skills/document-similarity)
- [PDFAPIHub documentation](https://pdfapihub.com/docs)
- [PDFAPIHub API](https://pdfapihub.com/api)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON response with similarity score, confidence, and selected comparison method]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a PDFAPIHub CLIENT-API-KEY header and accepts public URLs, base64 document payloads, or multipart file uploads.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
