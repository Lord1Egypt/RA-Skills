## Description: <br>
Publish social media posts to multiple platforms at once using Boring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and teams use this skill to publish or schedule text, image, and video posts across connected Facebook, Instagram, Threads, YouTube, TikTok, and X accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP Connector link contains an embedded authentication token and grants access to connected social accounts. <br>
Mitigation: Treat the MCP link like a password, share it only with trusted agents, and regenerate it if exposed. <br>
Risk: The connector can publish or schedule real posts on connected social media accounts. <br>
Mitigation: Connect only accounts the agent should use and ask for a final preview before posting or scheduling. <br>
Risk: Provided media may be uploaded to Boring-hosted storage so social platforms can access it for publishing. <br>
Mitigation: Avoid providing private media unless it is intended to be uploaded and published. <br>


## Reference(s): <br>
- [Boring MCP getting started documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html) <br>
- [Boring API documentation](https://boring-doc.aiagent-me.com) <br>
- [ClawHub skill page](https://clawhub.ai/snoopyrain/boring-social-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown summaries with connector tool calls and publishing results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include post IDs, scheduling times, per-platform success or failure details, and media upload URLs.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
