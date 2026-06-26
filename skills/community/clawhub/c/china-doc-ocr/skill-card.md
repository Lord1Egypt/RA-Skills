## Description: <br>
Recognizes complex documents, PDFs, scanned images, photos, invoices, receipts, ID cards, tables, and charts, then converts the extracted content to text, Markdown, or structured output using SiliconFlow OCR-capable models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and document-processing users use this skill to OCR Chinese and bilingual business documents, invoices, certificates, tables, charts, screenshots, and PDFs into readable Markdown or structured fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents, URLs, and prompts are sent to SiliconFlow for OCR processing. <br>
Mitigation: Use the skill only with documents allowed by the user's data policy and avoid highly confidential, regulated, or third-party documents unless SiliconFlow is approved for that use. <br>
Risk: OCR outputs and temporary files may persist in the workspace after processing. <br>
Mitigation: Delete saved OCR outputs and temporary workspace files after handling sensitive documents. <br>
Risk: The skill requires a SiliconFlow API key and may consume quota or incur billing. <br>
Mitigation: Use a limited API key where possible and monitor quota, billing, and request volume. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobewin/china-doc-ocr) <br>
- [Model selection reference](references/models.md) <br>
- [OCR prompt templates](references/prompts.md) <br>
- [SiliconFlow API endpoint](https://api.siliconflow.cn/v1/chat/completions) <br>
- [SiliconFlow API key portal](https://cloud.siliconflow.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, plain text, structured field summaries, or CSV-friendly tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save OCR results in the workspace; the OCR script defaults to high-detail image input and a 4096 token response cap unless changed by the user.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
