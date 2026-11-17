## Description:

Feishu File Manager helps agents read, download, and manage Feishu Drive files, including PDF, Word, PPT, and Excel content, by using Feishu tenant access tokens and Drive APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caspian9](https://clawhub.ai/user/caspian9)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to retrieve Feishu Drive files shared with an authorized Feishu app, download file content, parse common document formats, and return extracted content for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses local Feishu app secrets and tenant access tokens.

Mitigation: Use a dedicated least-privilege Feishu app, redact app secrets and tenant tokens from logs, and refresh or revoke tokens according to Feishu policy.

Risk: The documented scopes include broad and write-capable permissions for a mostly read and download workflow.

Mitigation: Remove write and broad scopes unless they are explicitly needed; prefer read-only and download-specific Feishu permissions.

Risk: Downloaded files may contain sensitive or unauthorized content.

Mitigation: Only access files the user specifically identifies and is authorized to retrieve, and clean up downloaded files after processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caspian9/skills/feishu-file-manager)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu Drive file download API](https://open.feishu.cn/open-apis/drive/v1/files/{file_token}/download)
- [Feishu Drive file metadata API](https://open.feishu.cn/open-apis/drive/v1/files/{file_token})
- [Feishu Drive folder listing API](https://open.feishu.cn/open-apis/drive/v1/files?parent_node={folder_token})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, Python, and bash snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include downloaded-file handling guidance and parsed document text from Feishu Drive files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
