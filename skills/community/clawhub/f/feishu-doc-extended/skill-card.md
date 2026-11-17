## Description:

Extends the OpenClaw Feishu document tool with image download URL retrieval and a manual Tesseract OCR workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xing2xian](https://clawhub.ai/user/xing2xian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to retrieve temporary image download URLs from Feishu documents and run OCR on captured images when Feishu document images need to be inspected as text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to persistently modify the built-in Feishu plugin and restart the OpenClaw gateway.

Mitigation: Review the plugin changes before applying them, keep a revert path, and only restart the gateway after confirming the modified plugin behavior is expected.

Risk: Returned image URLs, screenshots, and OCR text can expose sensitive Feishu document content.

Mitigation: Treat those artifacts as sensitive data, avoid sharing or logging them, and refresh expired temporary URLs only when needed.

Risk: The bundled Feishu schema may be broader than the documented image-download behavior and could confuse reviewers or installers.

Mitigation: Scope installation and review to the documented get_image behavior, or separate the broader schema changes before deployment.

Risk: OCR results can be incomplete or inaccurate when source images are unclear.

Mitigation: Verify important OCR output against the original image and prefer high-resolution screenshots.

## Reference(s):

- [Feishu Open Platform](https://open.feishu.cn)
- [ClawHub skill page](https://clawhub.ai/xing2xian/skills/feishu-doc-extended)
- [Changelog](references/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples, TypeScript snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The Feishu image URL returned by the modified tool is temporary; OCR quality depends on the captured image quality and local Tesseract setup.]

## Skill Version(s):

1.0.0 (source: release metadata, package.json, changelog released 2026-03-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
