## Description:

生成文本、URL 或 WiFi 信息的二维码，支持自定义尺寸、颜色和保存路径。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangzhenfu](https://clawhub.ai/user/yangzhenfu)

### License/Terms of Use:


## Use Case:

Developers and end users can use this skill to turn text, URLs, phone numbers, or WiFi configuration strings into QR-code images saved to a chosen file path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Loading the Python module may automatically install unpinned qrcode and Pillow packages, changing the user's Python environment without explicit setup control.

Mitigation: Review before installation, prefer pinned dependencies in a manifest or an explicit setup step, and run with limited filesystem, credential, and network access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangzhenfu/skills/generate-qr-code)
- [Publisher profile](https://clawhub.ai/user/yangzhenfu)

## Skill Output:

**Output Type(s):** [files, text, guidance]

**Output Format:** [PNG image file with a text status message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The QR image is saved to the requested path, or to a desktop path by default.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
