## Description:

Install and configure the native PaddleOCR plugin for DeepSeek Harness (DSH) from the Settings PaddleOCR GUI for OCR, image-to-text, PDF-to-Markdown, structured document parsing, endpoint setup, credential setup, verification, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aidenwu0209](https://clawhub.ai/user/aidenwu0209)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install and configure a DeepSeek Harness PaddleOCR plugin, then verify OCR endpoints, credentials, GUI visibility, and troubleshooting status for document and image parsing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow uses unpinned remote installation commands, so the code executed at install time can change after review.

Mitigation: Use a pinned package version and immutable commit SHA, review the plugin source before installation, and run setup in an isolated environment with minimum needed file access.

Risk: OCR service credentials could be exposed if entered outside the intended credential field.

Mitigation: Provide OCR credentials only through the DSH Credential field and avoid echoing, logging, or storing tokens in ordinary settings or source files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aidenwu0209/skills/dsh-paddleocr-skills-setup)
- [Project repository](https://github.com/Aidenwu0209/dsh-PaddleOCR-Skills)
- [PaddleOCR](https://www.paddleocr.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports prerequisite versions, installation commands, local web URL, visible configuration status, and any endpoint or credential values still required from the user.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
