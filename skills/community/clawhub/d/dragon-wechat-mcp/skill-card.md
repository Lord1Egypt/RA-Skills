## Description: <br>
Windows 电脑端微信消息监控与发送 MCP，实现在微信上给指定联系人发送消息 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dragon015](https://clawhub.ai/user/dragon015) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and users operating Windows desktop WeChat use this MCP server to let an agent check WeChat window status and send messages to the current or specified contact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send messages from the user's live WeChat session without reliable recipient confirmation. <br>
Mitigation: Keep WeChat on the intended chat, review the exact message before invoking the tool, and avoid using it around sensitive conversations. <br>
Risk: The skill may leave local screenshots of chat UI after testing or sending. <br>
Mitigation: Delete generated screenshot files after use and avoid running the skill when sensitive conversations are visible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dragon015/dragon-wechat-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/dragon015) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls] <br>
**Output Format:** [MCP JSON-RPC tool responses containing text or serialized JSON status data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can send messages through the user's active desktop WeChat session as an external side effect.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
