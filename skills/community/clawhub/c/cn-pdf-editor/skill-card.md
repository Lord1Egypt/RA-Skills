## Description:

本地PDF编辑工具，支持文本修改、图片插入、水印添加、批注、合并拆分、页面重排和签名，数据全程本地处理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document operators use this skill to launch a local web editor or CLI for modifying PDFs, adding watermarks and annotations, inserting images or signatures, and merging, splitting, reordering, rotating, deleting, or extracting pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The PDF editing web server exposes sensitive PDF viewing and editing endpoints on all network interfaces without authentication while describing itself as local-only.

Mitigation: Use only on a trusted machine and network, avoid opening sensitive PDFs while the server binds broadly, and prefer changing the server to localhost-only with authentication before routine use.

Risk: Delete, redaction, and save actions may permanently alter document content or produce edited copies that replace expected workflows.

Mitigation: Keep backup copies of source PDFs and review edited outputs before relying on or distributing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-pdf-editor)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files, JSON]

**Output Format:** [Markdown guidance with inline bash commands, JSON responses, and generated PDF or image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can launch a local web UI or run CLI actions that save edited PDFs, split outputs, extracted page images, and document metadata.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
