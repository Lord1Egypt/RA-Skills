## Description:

按公开规则处理 PDF、JPG 和 PNG 文件，供企业人员逐页确认敏感区域并生成复检后的对外副本。

This skill is ready for commercial/non-commercial use.

## Publisher:

[youteacher](https://clawhub.ai/user/youteacher)

### License/Terms of Use:

MIT-0

## Use Case:

企业团队使用此 Skill 按公开规则检查文件中的敏感信息，逐项决定处理范围，并生成供对外分享的脱敏副本。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded documents and generated copies are handled by a cloud service and retained for up to seven days.

Mitigation: Confirm the service’s privacy and retention terms suit the documents before uploading; keep API keys private.

Risk: Optional OCR and copy generation incur separate charges, and OCR sends selected pages to the stated model service.

Mitigation: Check current pricing and obtain separate explicit approval for selected-page OCR and generation before starting each paid step.

Risk: Redaction can miss sensitive content, and verification only covers the regions that were confirmed.

Mitigation: Review every page and candidate, confirm all regions manually, and inspect the final copy before sharing it.

## Reference(s):

- [上传、请求与轮询](https://ai-skills.open-idea.net/skill-docs/document-redaction/HTTP-REQUESTS.md)
- [操作字段与复核流程](https://ai-skills.open-idea.net/skill-docs/document-redaction/OPERATIONS.md)
- [平台密钥与费用](https://ai-skills.open-idea.net/skill-docs/document-redaction/API-KEY.md)
- [授权、隐私与人工复核](references/BEHAVIOR-RULES.md)

## Skill Output:

**Output Type(s):** [PDF files, PNG images, Guidance]

**Output Format:** [Image-based PDF or re-encoded PNG, with task guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Only user-confirmed regions are covered; generated copies do not retain searchable text, original attachments, or digital signatures.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
