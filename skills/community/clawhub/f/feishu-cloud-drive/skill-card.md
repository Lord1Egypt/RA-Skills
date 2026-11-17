## Description:

基于飞书官方 API 的云盘管理技能，支持文件列表查询、上传、下载、文件夹创建、权限管理、文件搜索、统计信息、快捷方式、复制移动等完整功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[han880520](https://clawhub.ai/user/han880520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace administrators use this skill to configure a Feishu app and let an agent manage Feishu Drive files and folders through Feishu's official APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload, download, share, move, copy, and delete Feishu Drive data using app credentials.

Mitigation: Use a dedicated least-privilege Feishu app and limit it to a test or approved root folder before enabling agent-driven operations.

Risk: Broad production Drive permissions could allow unintended file changes or disclosure if an agent receives an unsafe request.

Mitigation: Add external controls for user confirmation, allowed folders, upload and download paths, and audit logging before production use.

Risk: FEISHU_APP_SECRET is sensitive and grants access to tenant-level API actions configured for the app.

Mitigation: Store the secret only in environment or secret-management systems, rotate it periodically, and review permission grants before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/han880520/skills/feishu-cloud-drive)
- [Feishu Open Platform](https://open.feishu.cn)
- [Feishu Drive API documentation](https://open.feishu.cn/document/server-docs/docs/drive-v1)
- [Feishu Explorer API documentation](https://open.feishu.cn/document/server-docs/docs/drive-explorer)
- [Feishu permission member API documentation](https://open.feishu.cn/document/server-docs/docs/permission/permission-member/create)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell and Python examples; the Python client returns dictionary-style API responses and can read or write files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FEISHU_APP_ID and FEISHU_APP_SECRET; FEISHU_ROOT_FOLDER_TOKEN is optional for scoping operations to a default folder.]

## Skill Version(s):

1.1.5 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
