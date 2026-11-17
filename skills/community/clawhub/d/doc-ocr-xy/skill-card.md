## Description:

Scans PDF, OFD, and image documents, sends them to the Xiangyun NetOCR table OCR API, and returns recognized document content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liudengkui](https://clawhub.ai/user/liudengkui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to batch-recognize tables and text from document files through Xiangyun NetOCR, producing readable OCR output for single files or Markdown summaries for folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents selected for OCR are uploaded to a third-party NetOCR service.

Mitigation: Only process documents the user is authorized to upload, and review privacy or contractual requirements before using the service for sensitive content.

Risk: Xiangyun NetOCR credentials are stored in the skill directory as plaintext config.json.

Mitigation: Use non-production credentials when possible, restrict file access to the skill directory, and rotate credentials if the local environment is shared or compromised.

Risk: OCR use may incur provider charges.

Mitigation: Confirm the account, pricing, and batch size before running folder OCR jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liudengkui/skills/doc-ocr-xy)
- [NetOCR service](https://netocr.com)
- [Xiangyun OCR API reference](https://www.netocr.com/table.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text for single-file OCR and Markdown files for folder OCR, with shell commands for configuration and execution.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Xiangyun NetOCR credentials before OCR calls can run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
