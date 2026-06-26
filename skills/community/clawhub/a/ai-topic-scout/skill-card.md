## Description: <br>
AI Topic Scout tracks configured YouTube videos and Twitter/X posts from AI creators, analyzes cross-platform topic momentum, and writes scored short-video ideas and recommendations to DingTalk AI Tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agegr](https://clawhub.ai/user/agegr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content strategists, AI video teams, and workflow operators use this skill to collect creator activity from YouTube and Twitter/X, cluster emerging AI topics, and generate scored short-video topic recommendations for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live Twitter/X session credentials (`auth_token` and `ct0`), and passing them through command arguments can expose or misuse an account session. <br>
Mitigation: Prefer an official OAuth/API integration or a dedicated low-risk account, inject secrets through a protected secret manager or environment flow, avoid command-line cookie arguments, and rotate or revoke the session after use. <br>


## Reference(s): <br>
- [Setup Guide](references/setup-guide.md) <br>
- [Table Schema](references/table-schema.md) <br>
- [Operational Gotchas](references/gotchas.md) <br>
- [Configuration Template](references/config.json) <br>
- [DingTalk MCP Server](https://mcp.dingtalk.com/#/detail?mcpId=9555&detailType=marketMcpDetail) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with shell commands, JSON command arguments, and DingTalk AI Table records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces creator-content summaries, topic clusters, heat scores, background notes, and short-video topic suggestions for review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
