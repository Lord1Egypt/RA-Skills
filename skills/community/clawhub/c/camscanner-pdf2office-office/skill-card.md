## Description:

Use CamScanner to convert PDF documents to editable Word (.docx) or Excel (.xlsx) format while preserving the original formatting where supported.

This skill is ready for commercial/non-commercial use.

## Publisher:

[camscanner-ai](https://clawhub.ai/user/camscanner-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they need command-line guidance to upload a PDF to CamScanner, convert it into an editable Word or Excel file, and download the result locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends user PDFs to CamScanner's third-party servers for processing.

Mitigation: Confirm third-party document processing is allowed before use, and avoid confidential, regulated, or policy-restricted PDFs unless approved.

Risk: Incorrect input or output paths could upload the wrong document or overwrite an unintended local file.

Mitigation: Review the selected input PDF and output path before running the generated commands.

## Reference(s):

- [CamScanner Homepage](https://www.camscanner.com)
- [CamScanner PDF conversion API base URL](https://ai-tools.camscanner.com)
- [ClawHub skill listing](https://clawhub.ai/camscanner-ai/skills/camscanner-pdf2office-office)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command examples for upload, conversion, download, output extension selection, and basic error checks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
