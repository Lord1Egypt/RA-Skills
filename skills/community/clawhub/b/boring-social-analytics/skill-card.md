## Description: <br>
Track social media performance and engagement across Facebook, Instagram, Threads, YouTube, and TikTok using Boring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and social media operators use this skill to ask an agent for account performance, post analytics, publishing history, and cross-platform comparisons from connected Boring accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP Connector link contains an embedded authentication token and can grant access to connected analytics. <br>
Mitigation: Treat the MCP URL like a password, avoid sharing it, and regenerate it if exposed. <br>
Risk: Analytics requests are handled through Boring's service for connected social accounts. <br>
Mitigation: Install only if you trust Boring with analytics access, and review account disconnection and data retention controls. <br>


## Reference(s): <br>
- [Boring MCP setup documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html) <br>
- [Boring documentation](https://boring-doc.aiagent-me.com) <br>
- [Boring account and connector setup](https://boring.aiagent-me.com) <br>
- [ClawHub skill page](https://clawhub.ai/snoopyrain/boring-social-analytics) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown summaries and tables based on MCP tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include account summaries, ranked post metrics, cross-platform comparison tables, and error-handling guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
