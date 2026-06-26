## Description: <br>
Track Facebook Page performance and analytics, including reach, engagement, video views, and post-level metrics for a connected Facebook Page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and social media operators use this skill to review Facebook Page performance, compare post engagement, and summarize page or post metrics from a connected Boring MCP connector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP Connector URL contains an embedded authentication token. <br>
Mitigation: Treat the connector URL like a password, avoid sharing it publicly, and revoke or regenerate it if it is exposed. <br>
Risk: The connector can access Facebook Page analytics and account metadata through Boring. <br>
Mitigation: Install only after confirming that Boring is trusted for this data and that the requested Facebook permissions match the intended read-only analytics use. <br>
Risk: Analytics requests and returned metrics flow through a third-party service. <br>
Mitigation: Confirm the service's data handling is acceptable for the organization before connecting production Facebook Pages. <br>


## Reference(s): <br>
- [Facebook Analytics on ClawHub](https://clawhub.ai/snoopyrain/facebook-analytics) <br>
- [Boring MCP Connector Documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries and tables with metric explanations and connector guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference read-only Facebook Page analytics, account metadata, post metrics, and publishing history returned through the configured MCP connector.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
