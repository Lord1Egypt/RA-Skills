## Description: <br>
基于飞书官方 API 的云盘管理技能，支持文件列表查询、上传、下载、文件夹创建、权限管理、文件搜索、统计信息、快捷方式、复制移动等完整功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[han880520](https://clawhub.ai/user/han880520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to automate Feishu Drive file listing, upload, download, folder creation, search, copy, move, deletion, and sharing workflows through the Feishu Open Platform APIs. It is suited for agents that need governed cloud-drive operations with explicit credentials and scoped workspace access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform powerful Feishu Drive operations, including deletes, moves, sharing, uploads, and downloads. <br>
Mitigation: Use a dedicated Feishu app with minimum required scopes, set FEISHU_ROOT_FOLDER_TOKEN to restrict the working area, and confirm destructive or permission-changing actions before execution. <br>
Risk: FEISHU_APP_SECRET and access tokens can expose cloud-drive access if mishandled. <br>
Mitigation: Store credentials only in environment variables or a secrets manager, avoid committing them to source control, and rotate them according to the organization's credential policy. <br>
Risk: Contact lookup and access-record operations can expose sensitive workplace identity and activity data. <br>
Mitigation: Limit use to necessary workflows, restrict returned data handling, and avoid logging contact lookup results or access records unless approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/han880520/feishu-cloud-drive) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>
- [Feishu Drive permission FAQ](https://open.feishu.cn/document/server-docs/docs/drive-v1/faq#b02e5bfb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, modify, move, share, upload, download, or delete Feishu Drive files and folders when the agent executes the provided API operations.] <br>

## Skill Version(s): <br>
1.1.5 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
