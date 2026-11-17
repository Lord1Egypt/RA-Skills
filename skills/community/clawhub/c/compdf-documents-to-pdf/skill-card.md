## Description:

Convert Word, Excel, PPT, HTML, TXT, CSV, RTF, PNG, and JPG files into PDF with ComPDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[compdf-youna](https://clawhub.ai/user/compdf-youna)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare accurate ComPDF Server API request plans for converting supported office documents, data files, HTML, and images into PDF for sharing, approvals, printing, or archiving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A reusable ComPDF API key is stored in a plaintext skill-local api_key file.

Mitigation: Use a low-privilege key if supported, keep the file out of version control and publishing, and rotate the key if it may have been exposed.

Risk: Selected documents are sent to ComPDF for processing.

Mitigation: Confirm uploads before sending files and avoid sensitive or regulated documents unless ComPDF's terms and retention practices fit the intended use.

Risk: The artifact includes broad ComPDF API documentation beyond the supported document-to-PDF conversion scope.

Mitigation: Use only the supported conversion endpoints listed by the skill and avoid PDF editing, PDF-to-document conversion, and other non-conversion endpoints.

## Reference(s):

- [ComPDF Endpoint Index](artifact/references/endpoint-index.md)
- [Official ComPDF V2 API Reference Snapshot](artifact/references/official-api-reference.md)
- [ComPDF API Overview](https://www.compdf.com/guides/api-reference/v2/api-overview)
- [ComPDF Authentication](https://www.compdf.com/guides/api-reference/v2/authentication)
- [ComPDF Request Workflow](https://www.compdf.com/guides/api-reference/v2/request-workflow)
- [ComPDF Portal](https://www.compdf.com/compdf-portal/signin?utm_source=clawhub&utm_medium=referral&utm_campaign=compdf_skills_repo_en&ref_platform_id=clawhub_compdfkit_skills_en)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown with endpoint, method, request fields, response fields, and follow-up polling or download steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ComPDF API request details, but should not display, log, or include stored API keys in examples.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
