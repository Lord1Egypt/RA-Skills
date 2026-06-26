## Description: <br>
Finance OCR Pro extracts structured Markdown, HTML, DOCX, and Excel from scanned documents, images, and office files by sending rendered page images and OCR prompts to a configured OpenAI-compatible vision-language model endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rizmoon](https://clawhub.ai/user/rizmoon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to OCR and convert visually complex financial documents such as annual reports, prospectuses, regulatory filings, research reports, and investor presentations into reviewable and editable outputs. It is best suited to documents with dense tables, charts, graphs, formulas, footnotes, and multi-part layouts where plain text extraction is insufficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OCR sends rendered document page images and prompts to the configured BASE_URL, which may expose sensitive financial or internal content to that endpoint. <br>
Mitigation: Use a trusted local or approved provider endpoint for sensitive files and verify BASE_URL before running OCR. <br>
Risk: The required API_KEY is a sensitive credential. <br>
Mitigation: Keep API_KEY out of shared files, use local environment configuration, and do not commit populated .env files. <br>
Risk: Generated HTML reports are derived from document content and may contain sensitive or untrusted content. <br>
Mitigation: Review generated HTML before sharing or opening broadly, especially for confidential source documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rizmoon/finance-ocr-pro) <br>
- [Publisher profile](https://clawhub.ai/user/rizmoon) <br>
- [README](artifact/README.md) <br>
- [Security notes](artifact/SECURITY.md) <br>
- [Third-party notices](artifact/THIRD_PARTY_NOTICES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated document artifacts including Markdown, HTML, DOCX, and Excel] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires API_KEY, BASE_URL, and VLM_MODEL; default execution uses a local background OCR job and one OCR thread unless the configured endpoint supports safe parallel requests.] <br>

## Skill Version(s): <br>
1.0.7 (source: frontmatter, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
