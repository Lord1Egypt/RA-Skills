## Description: <br>
Extends Feishu document workflows with image download URL retrieval and OCR guidance using Tesseract with the OpenClaw Feishu plugin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xing2xian](https://clawhub.ai/user/xing2xian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to retrieve temporary image URLs from Feishu document image blocks, then run OCR on captured images with Tesseract. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release asks users to persistently patch the built-in OpenClaw Feishu plugin. <br>
Mitigation: Back up original plugin files, review that only the intended get_image schema and implementation are added, and test in a controlled environment before normal use. <br>
Risk: Returned image URLs, browser screenshots, and OCR output can expose sensitive Feishu document data. <br>
Mitigation: Keep Feishu app permissions minimal, restrict document access, avoid sharing temporary URLs, and treat screenshots and OCR text as sensitive data. <br>
Risk: The security summary notes broader document-management schema than the public description explains. <br>
Mitigation: Review the full included schema and confirm enabled Feishu actions match the intended deployment scope before installing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xing2xian/feishu-doc-extended) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>
- [CHANGELOG](references/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with TypeScript snippets, shell commands, and JSON tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Feishu plugin, Tesseract OCR, Feishu app permissions, and handling of temporary image URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, package.json, and CHANGELOG; released 2026-03-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
