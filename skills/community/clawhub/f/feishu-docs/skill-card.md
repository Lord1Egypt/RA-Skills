## Description:

飞书文档(Docx)API技能，用于创建、读取、更新和删除飞书文档，并支持Markdown/HTML内容转换和文档权限管理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenlikewatermelon](https://clawhub.ai/user/stevenlikewatermelon)

### License/Terms of Use:

MIT

## Use Case:

Developers and operations teams use this skill to manage Feishu Docx documents from an agent or CLI, including document CRUD, Markdown/HTML conversion, search/list operations, and collaborator permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete documents or replace the full contents of shared Feishu documents.

Mitigation: Test in a non-production folder first, manually confirm document IDs before delete or full-replace operations, and prefer append or read-only workflows where possible.

Risk: Feishu app credentials may grant read/write access to documents.

Mitigation: Use a least-privileged Feishu app with only the permissions needed for the intended workflow.

Risk: Passing app secrets with --app-secret can expose credentials through shell history or process inspection.

Mitigation: Prefer protected environment configuration for FEISHU_APP_SECRET and avoid command-line secret arguments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stevenlikewatermelon/skills/feishu-docs)
- [Feishu Open Platform](https://open.feishu.cn/app)
- [Feishu Docx API overview](https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/overview)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, JSON, Text, Configuration]

**Output Format:** [Markdown/text/JSON CLI output and shell commands that call the Feishu Docs API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FEISHU_APP_ID and FEISHU_APP_SECRET; operations may create, update, delete, search, list, export, or share Feishu documents.]

## Skill Version(s):

1.1.1 (source: evidence.release.version, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
