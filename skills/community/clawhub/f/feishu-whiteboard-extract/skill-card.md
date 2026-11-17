## Description:

Extracts image node file tokens from Feishu Whiteboards and supports media download or full-board image export for OCR and archiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forevershu](https://clawhub.ai/user/forevershu)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to extract Feishu whiteboard image node tokens, download the related media, and export a full-board image for OCR, review, and archival workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Feishu app credentials and can retrieve whiteboard contents.

Mitigation: Install only when the publisher is trusted, use least-privilege Feishu app credentials, and do not paste app secrets, tokens, cookies, or webhooks into chat.

Risk: The raw node exporter can expose more board data than image file tokens.

Mitigation: Use export_nodes_raw.js only when full node data is explicitly needed, and review exported JSON for sensitive content before sharing or archiving.

Risk: The security evidence flags unsafe file and dependency handling.

Mitigation: Constrain output paths and regenerate or update dependencies from a trusted HTTPS registry before operational use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/forevershu/skills/feishu-whiteboard-extract)
- [Feishu Tenant Access Token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands; scripts emit structured JSON, downloaded media files, and full-board SVG/PNG/JPG exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Feishu whiteboard ID and Feishu app credentials with access to the target whiteboard.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
