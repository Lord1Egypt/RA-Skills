## Description:

Use when OCR-specialized extraction is needed with Alibaba Cloud Model Studio Qwen OCR models (`qwen-vl-ocr`, `qwen-vl-ocr-latest`, and snapshots), including document parsing, table parsing, multilingual OCR, formula recognition, and key information extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare Alibaba Cloud Model Studio Qwen OCR requests for document text extraction, table parsing, multilingual OCR, formula recognition, and key information extraction. It is suited to OCR-first workflows where document structure and extracted fields matter more than broad visual reasoning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive or regulated documents may be routed through third-party cloud OCR workflows.

Mitigation: Review the skill before installation for confidential workflows, redact sensitive content where possible, and use controlled or short-lived access methods for document inputs.

Risk: Making private files publicly accessible for OCR can expose document contents.

Mitigation: Avoid public URLs for private files where possible, prefer protected access or data URLs, and clean up output/aliyun-qwen-ocr/ after runs that include private payloads.

Risk: OCR output for critical business fields can be incorrect or incomplete.

Mitigation: Add downstream validation rules for critical extracted fields before relying on the results in business workflows.

## Reference(s):

- [Qwen OCR API Reference Notes](references/api_reference.md)
- [Qwen OCR Sources](references/sources.md)
- [Alibaba Cloud Qwen OCR Documentation](https://help.aliyun.com/zh/model-studio/qwen-vl-ocr)
- [Alibaba Cloud Qwen OCR API Reference](https://help.aliyun.com/zh/model-studio/qwen-vl-ocr-api-reference)
- [Alibaba Cloud Model Updates](https://help.aliyun.com/zh/model-studio/newly-released-models)
- [Alibaba Cloud Model List](https://help.aliyun.com/zh/model-studio/models)
- [ClawHub Skill Page](https://clawhub.ai/cinience/skills/aliyun-qwen-ocr)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and generated JSON request payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Request payloads, selected task names, model choices, and normalized output expectations are saved under output/aliyun-qwen-ocr/ by default.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
