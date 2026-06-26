## Description: <br>
创建飞书云文档。从 Lark-flavored Markdown 内容创建新的飞书云文档，支持指定创建位置（文件夹/知识库/知识空间）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a3152557994-ship-it](https://clawhub.ai/user/a3152557994-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Feishu users and agents use this skill to create cloud documents from Lark-flavored Markdown, including structured content such as callouts, tables, media links, and diagrams. It supports creating documents in a personal folder, a knowledge base node, or a knowledge space. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Markdown content, linked media, mentions, reminders, and created documents may be written to Feishu under the connected account's permissions. <br>
Mitigation: Use only trusted Feishu MCP/account connections and avoid submitting secrets or private data unless that content is intended to be created in Feishu. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/a3152557994-ship-it/feishu-doc-create) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, API Calls, Guidance] <br>
**Output Format:** [JSON result containing doc_id, doc_url, and message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a Feishu cloud document through the connected Feishu MCP/account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
