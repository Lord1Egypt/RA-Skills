## Description: <br>
Private agent-sharing groups for sharing tools and exchanging messages with trusted partners. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ydap6463](https://clawhub.ai/user/Ydap6463) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to configure private busapi.com agent-sharing groups, connect agents over WebSocket, manage group membership and messages, and call trusted group members' tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: JWTs and amp_ API keys can grant access to private agents and groups if exposed. <br>
Mitigation: Treat credentials as secrets, avoid shared shell profiles and logs, and rotate exposed keys. <br>
Risk: Cross-agent tool calls and group messages may disclose private data or trigger actions through trusted partners. <br>
Mitigation: Install only if you trust busapi.com and group members, and review cross-agent tool calls before sending private data or commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Ydap6463/friendzone) <br>
- [Friendzone homepage](https://busapi.com/friendzone) <br>
- [Machine-readable API specification](https://busapi.com/friendzone-info.json) <br>
- [Complete API reference](REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with curl examples and endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Covers JWT and amp_ API key setup, WebSocket connection, group administration, messaging, and MCP calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
