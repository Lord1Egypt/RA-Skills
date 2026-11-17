## Description:

创建飞书云文档。从 Lark-flavored Markdown 内容创建新的飞书云文档，支持指定创建位置（文件夹/知识库/知识空间）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[a3152557994-ship-it](https://clawhub.ai/user/a3152557994-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to create persistent Feishu cloud documents from Lark-flavored Markdown, optionally placing them in a personal folder, wiki node, or knowledge space.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates persistent documents in a Feishu workspace and can include referenced public image or file URLs.

Mitigation: Review sensitive content before creation, specify the intended target folder or wiki location, and use only trusted public media URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/a3152557994-ship-it/skills/feishu-doc-create)

## Skill Output:

**Output Type(s):** [Markdown, JSON, API Calls, Files]

**Output Format:** [Lark-flavored Markdown input and structured JSON result containing document ID, URL, and status message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent Feishu documents and may fetch referenced public media URLs for upload into the workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
