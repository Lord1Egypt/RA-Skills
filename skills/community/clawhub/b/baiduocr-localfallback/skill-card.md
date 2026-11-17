## Description:

Provides Baidu OCR API usage guidance with EasyOCR local fallback, image preprocessing, token caching, and retry behavior for text recognition workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xx235300](https://clawhub.ai/user/xx235300)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure and operate Baidu OCR-backed text recognition across documents, receipts, ID cards, handwriting, tables, and other image inputs, with local EasyOCR fallback when remote OCR is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and setup flows handle Baidu OCR API keys and may store them in a local plaintext config file.

Mitigation: Prefer environment variables; if using the config file, restrict permissions to owner-only and avoid sharing files or logs containing credentials.

Risk: Images sent to Baidu OCR may contain sensitive document content and are processed by a third-party cloud service.

Mitigation: Process sensitive documents only when Baidu Cloud privacy and retention terms are acceptable; otherwise avoid remote OCR or use local fallback where suitable.

Risk: One-click remote installation and unpinned Python dependencies can change what code is installed over time.

Mitigation: Review before installing, prefer the included local installer from the release artifact, and use a virtual environment with pinned dependencies.

## Reference(s):

- [Baidu Cloud OCR Documentation](https://cloud.baidu.com/doc/OCR/s/Ck3h7y2ia)
- [ClawHub skill page](https://clawhub.ai/xx235300/skills/baiduocr-localfallback)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python, JSON, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OCR response schemas, credential configuration steps, and local fallback behavior notes.]

## Skill Version(s):

1.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
