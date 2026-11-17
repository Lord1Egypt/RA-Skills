## Description:

Generate a PDF document from HTML content or a public URL with support for custom page sizes, fonts, margins, viewport dimensions, dynamic parameter substitution, and multiple output formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rishabhdugar](https://clawhub.ai/user/rishabhdugar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to convert HTML templates or public web pages into PDFs for invoices, reports, certificates, receipts, and archival snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML, CSS, dynamic parameters, public URLs, and generated PDFs may be processed by or stored with pdfapihub.com.

Mitigation: Use only data approved for that provider and avoid secrets, internal-only URLs, regulated personal data, contracts, invoices, or customer records unless the provider is approved for that data.

Risk: Generated PDFs may expose sensitive rendered content through returned URLs or downloadable files.

Mitigation: Treat generated PDF links and files as externally hosted outputs and apply appropriate access, sharing, and retention controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rishabhdugar/skills/generate-pdf)
- [PDF API Hub documentation](https://pdfapihub.com/docs)
- [PDF API Hub](https://pdfapihub.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [JSON API request guidance and PDF output as a URL, base64 string, or binary file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a pdfapihub.com API key; output retention and page limits are provider dependent.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
