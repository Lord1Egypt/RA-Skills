## Description: <br>
Converts scanned PDFs, images, OFD files, receipts, contracts, court documents, and other files that the agent cannot read natively into text or Markdown using Deli Legal OCR as a fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolalam](https://clawhub.ai/user/coolalam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and document-review workflows use this skill when native file parsing fails or when the user explicitly requests Deli OCR. It produces Markdown or text from scanned documents so downstream analysis, evidence organization, contract review, or legal drafting can continue. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected files are uploaded to the Deli Legal OCR service or a configured compatible endpoint. <br>
Mitigation: Use the skill only when policy permits third-party processing of the selected files, and avoid confidential legal, financial, medical, or personal documents unless that processing is approved. <br>
Risk: OCR output may misread critical fields such as amounts, dates, names, case numbers, invoices, or bank details. <br>
Mitigation: Review OCR results carefully before relying on extracted values in analysis, filings, payments, or records. <br>
Risk: The skill requires an API key or compatible credential configuration. <br>
Mitigation: Configure credentials only in the intended config or environment mechanism and rotate them according to local credential-management policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coolalam/deli-ocr-file-parser) <br>
- [Deli Legal API key setup](https://open.delilegal.com/personal/keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files with optional JSON OCR response files and concise command-line status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes one Markdown file per parsed input and can save the raw OCR response JSON when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
