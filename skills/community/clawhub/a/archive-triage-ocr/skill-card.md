## Description:

纸质票据 vs APP 截图分类归档规范：判断标准、OCR 落盘、时间线索引、定期核对。脱敏通用规则。

This skill is ready for commercial/non-commercial use.

## Publisher:

[adchina2025](https://clawhub.ai/user/adchina2025)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to decide which receipt images and app screenshots should be archived, OCRed, indexed, registered, or ignored in a personal document archive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OCR sidecars and timeline indexes can expose sensitive personal records.

Mitigation: Keep generated OCR text and metadata in a private or encrypted location.

Risk: Cloud OCR can send personal documents outside the local archive.

Mitigation: Prefer local OCR and use cloud OCR only after explicit user approval.

Risk: Uncertain screenshots may be incorrectly deleted or archived.

Mitigation: Move uncertain items to a temporary review area and require user confirmation before final disposition.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/adchina2025/skills/archive-triage-ocr)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with recommended OCR sidecar metadata and timeline index formats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Treats OCR text and timeline metadata as sensitive personal records.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
