## Description:

PDF文档处理工具（含OCR）。本地处理PDF文件，支持文本提取、智能摘要、表格导出、关键词问答、PDF拆分、OCR扫描版识别。纯本地处理，保护文档隐私。

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and document reviewers use this skill to run local PDF extraction, summarization, table discovery, keyword question answering, page splitting, and OCR workflows for Chinese and English documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local PDF files and can generate output files, including split PDFs and plaintext OCR text.

Mitigation: Use it only on documents you are comfortable processing locally, choose explicit output locations for sensitive files, and delete generated plaintext OCR results when they are no longer needed.

Risk: OCR and keyword-based summaries or answers may be incomplete or inaccurate for low-quality scans or complex documents.

Mitigation: Review extracted text, OCR confidence, and generated summaries before relying on them for legal, financial, or other high-impact decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-pdf-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Console text and JSON status, with optional generated PDF and TXT files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes local PDF files and may write split PDFs or plaintext OCR output to disk.]

## Skill Version(s):

1.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
