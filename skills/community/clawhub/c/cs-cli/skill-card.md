## Description:

Use CamScanner through an agent with natural-language requests to find, organize, and process documents more easily. You can start with documents in your CamScanner account, or upload local files to use cloud capabilities such as image enhancement, OCR, format conversion, and image authenticity checks. A CamScanner account login is required to use these features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[camscanner-ai](https://clawhub.ai/user/camscanner-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams can use an agent to search and organize CamScanner documents, or process local files through CamScanner for OCR, image enhancement, conversion, translation, and authenticity checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local files are uploaded to CamScanner for cloud processing, even when results are saved locally; cloud-save options can also create persistent account copies.

Mitigation: Process only documents approved for CamScanner cloud handling. For local-only results, specify a local output and omit the cloud-save option.

Risk: Usage reporting may disclose full requests and commands, and updates can replace both the CLI and skill files.

Mitigation: Keep reporting optional and minimize shared content. Require user approval before updates and verify both the software and skill packages before replacement.

## Reference(s):

- [CamScanner](https://www.camscanner.com)
- [CamScanner skill release on ClawHub](https://clawhub.ai/camscanner-ai/skills/cs-cli)
- [batch-convert.md](artifact/references/batch-convert.md)
- [cloud-documents.md](artifact/references/cloud-documents.md)
- [image-enhance.md](artifact/references/image-enhance.md)
- [image-processing.md](artifact/references/image-processing.md)
- [ocr-extract.md](artifact/references/ocr-extract.md)
- [office-processing.md](artifact/references/office-processing.md)
- [pdf-processing.md](artifact/references/pdf-processing.md)
- [tool-combos.md](artifact/references/tool-combos.md)
- [translate.md](artifact/references/translate.md)
- [watermark-protection.md](artifact/references/watermark-protection.md)

## Skill Output:

**Output Type(s):** [Files, Text, Markdown, JSON]

**Output Format:** [Processed image, PDF, and Office files; extracted text or Markdown; and structured JSON, depending on the requested operation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may be saved locally, to the CamScanner account, or both, depending on the selected options.]

## Skill Version(s):

1.1.9 (source: artifact/SKILL.md frontmatter; server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
