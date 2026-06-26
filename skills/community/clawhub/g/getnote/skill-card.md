## Description: <br>
Connects an agent to Get笔记 so users can save text, links, and images as notes, search notes semantically, and manage knowledge bases, tags, note updates, deletion, and sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iswalle](https://clawhub.ai/user/iswalle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to record, retrieve, organize, update, delete, and share personal Get笔记 notes and knowledge-base content through natural-language requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent credentials can grant ongoing access to a user's private Get笔记 account. <br>
Mitigation: Install only when comfortable granting this access, keep API keys out of chat, and store credentials through the documented configuration flow. <br>
Risk: The skill can read, modify, delete, and publicly share private notes. <br>
Mitigation: Use explicit commands for sensitive actions, verify note contents before sharing, and configure GETNOTE_OWNER_ID in shared or group contexts. <br>
Risk: Broad natural-language triggers may perform unintended save, search, delete, or share operations. <br>
Mitigation: Ask for confirmation when intent is ambiguous or destructive, and report success only after the Get笔记 API response confirms the action. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/iswalle/getnote) <br>
- [Get笔记 Homepage](https://biji.com) <br>
- [Get笔记 Open API](https://www.biji.com/openapi) <br>
- [README](README.md) <br>
- [Get笔记 API 详细参考](references/api-details.md) <br>
- [保存笔记](references/save.md) <br>
- [语义搜索](references/search.md) <br>
- [笔记列表与详情](references/list.md) <br>
- [知识库管理](references/knowledge.md) <br>
- [标签管理](references/tags.md) <br>
- [授权配置](references/oauth.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or text responses with optional JSON snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Get笔记 API credentials; actions may read, create, update, delete, or share user notes.] <br>

## Skill Version(s): <br>
1.8.8 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
