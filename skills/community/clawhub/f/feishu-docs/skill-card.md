## Description: <br>
飞书文档(Docx)API技能，用于创建、读取、更新和删除飞书文档，并支持 Markdown/HTML 内容转换和文档权限管理。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[StevenLikeWatermelon](https://clawhub.ai/user/StevenLikeWatermelon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to create, read, update, delete, search, export, and share Feishu Docs content from CLI or JavaScript API workflows using configured Feishu app credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete, overwrite, or share Feishu cloud documents. <br>
Mitigation: Verify document IDs, folder tokens, recipients, and intended permissions before delete, replace, or share commands, and keep backups or version history for important documents. <br>
Risk: The skill requires Feishu app credentials and document access permissions. <br>
Mitigation: Use a least-privilege Feishu app, protect FEISHU_APP_SECRET, rotate credentials when needed, and avoid tenant-wide document access unless required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/StevenLikeWatermelon/feishu-docs) <br>
- [Feishu Docx API overview](https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/overview) <br>
- [Feishu Open Platform app console](https://open.feishu.cn/app) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Code, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and JavaScript API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FEISHU_APP_ID and FEISHU_APP_SECRET; commands can create, modify, delete, or share Feishu documents.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
