## Description:

Batch convert files between CSV, Excel, JSON, PDF, Markdown, DOCX, HTML, PNG, JPG, and TXT formats with encoding handling, quota tiers, and optional Feishu delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffersplind92](https://clawhub.ai/user/jeffersplind92)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and document-heavy teams use this skill to batch convert uploaded files across common spreadsheet, document, image, and data formats. It can be used for local conversion workflows and optional delivery of conversion results through Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send accepted-prefix environment credential values to a third-party validation service.

Mitigation: Run it without OPENAI_API_KEY set unless token validation through YK Global is explicitly intended.

Risk: Converted document names, status details, or attachments may be delivered through Feishu when that integration is enabled.

Mitigation: Use Feishu delivery only with approved destinations and non-sensitive payloads.

Risk: The skill caches account-related validation metadata locally.

Mitigation: Review and clear the local converter cache after use in shared or sensitive environments.

Risk: Unpinned dependencies and OCR/document-processing packages can change behavior across installs.

Mitigation: Pin and review dependencies before installing in production environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeffersplind92/skills/document-format-converter)
- [Publisher profile](https://clawhub.ai/user/jeffersplind92)
- [Artifact README](artifact/README.md)
- [Artifact SKILL](artifact/SKILL.md)
- [Tesseract OCR setup reference](https://github.com/UB-Mannheim/tesseract/wiki)
- [YK-Global purchase link](https://yk-global.com)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Converted files with JSON status summaries and Markdown or command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports batch input files, target format selection, output directory selection, subscription tier checks, OCR-related dependencies, and optional Feishu notifications.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-04-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
