## Description:

Add a text watermark to one or multiple PDFs by uploading them to the Solutions API, polling until completion, then returning download URL(s) for the watermarked PDF(s) or a ZIP if multiple files are processed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crossservicesolutions](https://clawhub.ai/user/crossservicesolutions)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to watermark one or more PDF files through the Solutions API and receive structured download links for the processed PDFs or ZIP output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDFs, watermark text, and the API key are sent to a third-party service.

Mitigation: Use only when the provider's retention, access, and deletion practices are acceptable for the selected documents; avoid confidential, regulated, or customer documents unless approved.

Risk: A base URL override could disclose PDFs and credentials to the wrong endpoint.

Mitigation: Keep --base-url and SOLUTIONS_BASE_URL locked to a trusted HTTPS Solutions API endpoint.

Risk: Bearer API keys can grant access to the external service if exposed.

Mitigation: Provide API keys through secrets or environment variables and do not echo or log them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crossservicesolutions/skills/add-watermark-to-pdf)
- [Solutions API watermark endpoint](https://api.xss-cross-service-solutions.com/solutions/solutions/api/61)

## Skill Output:

**Output Type(s):** [text, files]

**Output Format:** [JSON object with job status, output file metadata, and download URL(s)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return one or more PDF download URLs or a ZIP download URL for batch output.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
