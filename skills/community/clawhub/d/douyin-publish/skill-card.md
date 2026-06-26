## Description: <br>
Helps an agent log in to Douyin Creator Platform, upload videos, publish them, manage tags, and check publishing status through configured MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gonghaiquan](https://clawhub.ai/user/gonghaiquan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators and operators use this skill to publish videos to Douyin from an agent conversation after configuring the required MCP server and account login. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent publish content through a real Douyin account. <br>
Mitigation: Use a dedicated creator account where possible and require final human confirmation before upload or publish actions. <br>
Risk: The workflow relies on a referenced external MCP server and persistent login cookies. <br>
Mitigation: Install only if the MCP server is trusted, pin or review the server, and protect or delete saved cookie files when they are not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gonghaiquan/douyin-publish) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Douyin MCP server and an authenticated Douyin creator account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
