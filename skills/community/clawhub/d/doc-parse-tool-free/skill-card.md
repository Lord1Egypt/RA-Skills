## Description:

通用文档解析工具，支持PDF、图片、扫描件的结构化信息提取与OCR识别。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to parse PDFs, images, and scanned documents into structured outputs, OCR text, and extracted tables for single-document or daily document workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can involve command execution, file access, and external OCR or API services while handling potentially sensitive documents.

Mitigation: Review each proposed command before running it, prefer local-only processing for sensitive content, and avoid confidential, legal, financial, medical, or proprietary documents unless processing paths are fully understood.

Risk: OCR and document extraction may produce incomplete or incorrect structured data, especially for scans, images, or tables.

Mitigation: Validate extracted text and tables against the source document before using results in downstream decisions or records.

Risk: API keys or document contents could be exposed if copied into commands, logs, or cloud services.

Mitigation: Use environment variables for credentials, avoid hardcoding secrets, and redact sensitive inputs and outputs before sharing logs.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks and JSON or YAML configuration examples; parsed document results may be structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local files, command execution, and OCR or API services depending on the agent environment.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
