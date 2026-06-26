## Description: <br>
Generate a PDF document from HTML content or a public URL, with support for custom page sizes, fonts, margins, viewport dimensions, dynamic parameter substitution, and multiple output formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rishabhdugar](https://clawhub.ai/user/rishabhdugar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate PDFs from HTML templates or public URLs for invoices, reports, certificates, contracts, receipts, and webpage snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected HTML, CSS, dynamic values, or public webpage URLs are sent to pdfapihub.com for PDF rendering. <br>
Mitigation: Avoid secrets, internal-only URLs, regulated data, or confidential documents unless your organization has approved pdfapihub.com and its retention policy. <br>
Risk: The skill requires a PDF API Hub API key. <br>
Mitigation: Store the API key in an approved secret manager or environment variable and avoid exposing it in prompts, shared logs, examples, or generated documents. <br>


## Reference(s): <br>
- [Generate PDF from HTML on ClawHub](https://clawhub.ai/rishabhdugar/generate-pdf) <br>
- [PDF API Hub Documentation](https://pdfapihub.com/docs) <br>
- [PDF API Hub](https://pdfapihub.com) <br>


## Skill Output: <br>
**Output Type(s):** [PDF files, URLs, Base64 data, Shell commands, Guidance] <br>
**Output Format:** [API request guidance and JSON responses containing a PDF URL, base64 PDF data, or raw PDF output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a CLIENT-API-KEY header and either html_content or a public url, with optional CSS, dynamic parameters, page size, margins, viewport, font, wait time, and filename settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
