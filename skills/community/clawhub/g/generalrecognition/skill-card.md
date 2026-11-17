## Description:

This skill uses JisuAPI general text recognition OCR to extract text from local or base64-encoded images, with support for Chinese, English, and several other languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a user asks to OCR a screenshot or photo and return the recognized text for follow-up formatting, analysis, or translation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images may be uploaded to JisuAPI for OCR, which can expose sensitive content.

Mitigation: Do not use this skill on screenshots or files containing passwords, personal records, internal documents, or regulated data unless external OCR processing is approved.

Risk: Local path inputs can select files for upload, and the security evidence reports weak file-boundary checks.

Mitigation: Use only intended image files and harden path, symlink, file-type, and size validation before deployment.

## Reference(s):

- [JisuAPI General Text Recognition Documentation](https://www.jisuapi.com/api/generalrecognition/)
- [JisuAPI Provider Site](https://www.jisuapi.com/)
- [ClawHub Skill Page](https://clawhub.ai/jisuapi/skills/generalrecognition)
- [ClawHub Publisher Profile](https://clawhub.ai/user/jisuapi)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON from the OCR script, typically converted by the agent into plain text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; local images or base64 image data are sent to JisuAPI for OCR.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
