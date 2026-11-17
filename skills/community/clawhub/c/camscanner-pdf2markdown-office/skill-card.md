## Description:

CamScanner-Pdf2Markdown helps agents convert PDF documents into Markdown by uploading the PDF to CamScanner's hosted conversion service and downloading the resulting Markdown file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[camscanner-ai](https://clawhub.ai/user/camscanner-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge workers, and agents use this skill to convert PDFs into editable Markdown for extraction, summarization, and downstream LLM processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDFs are sent to CamScanner's hosted service for conversion.

Mitigation: Use only when external processing is acceptable; avoid confidential, regulated, or highly sensitive documents unless that data flow has been approved.

Risk: The workflow depends on remote service availability and correct upload, convert, and download responses.

Mitigation: Check each response before proceeding and confirm the Markdown output before using it for downstream analysis or summarization.

## Reference(s):

- [CamScanner homepage](https://www.camscanner.com)
- [CamScanner hosted conversion API](https://ai-tools.camscanner.com)
- [ClawHub skill listing](https://clawhub.ai/camscanner-ai/skills/camscanner-pdf2markdown-office)
- [CamScanner publisher profile](https://clawhub.ai/user/camscanner-ai)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance, Files]

**Output Format:** [Markdown file with command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; converted output is saved to a local path selected by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
