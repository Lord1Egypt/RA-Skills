## Description: <br>
为智能体提供飞书文档读写能力：导出全文、读取评论与段落、写回修改并回复评论。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jachian-lee](https://clawhub.ai/user/Jachian-lee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent read Feishu document comments and paragraph text, export document context as Markdown, write approved edits back to document blocks, and reply to or resolve comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live Feishu document edits, delete selected text, insert summaries, reply to comments, and mark comments resolved. <br>
Mitigation: Require the agent to preview proposed edits and get user approval before any update, delete, summarize, reply, or resolve operation. <br>
Risk: Feishu credentials may allow access beyond the intended document scope if the application is broadly authorized. <br>
Mitigation: Use a dedicated Feishu app with the minimum required permissions and grant it only to the documents intended for review. <br>
Risk: The shell wrapper has unsafe argument handling for user-supplied document tokens, block IDs, and text. <br>
Mitigation: Prefer the MCP tools or direct Python entry points, and avoid run-tool.sh until its argument handling is fixed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Jachian-lee/feishu-doc-reviewer) <br>
- [Feishu Open Platform](https://open.feishu.cn/app/) <br>
- [Feishu Open API base](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, API Calls, Shell commands, Configuration] <br>
**Output Format:** [JSON tool responses, Markdown document exports, command output, and Feishu document or comment updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu application credentials and document-level authorization for read, edit, comment, and resolve operations.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
