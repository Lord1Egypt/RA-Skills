## Description: <br>
Publish posts to Facebook Pages, including text, photo, album, video, scheduled posts, and scheduled-post management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and social media operators use this skill to publish or schedule text, photo, album, and video posts to connected Facebook Pages through Boring after confirming the target Page, content, media, and timing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Boring MCP connector link contains an embedded token that grants posting access to connected Facebook Pages. <br>
Mitigation: Treat the connector link like a password, share it only with trusted agents, connect only the Pages needed, and revoke or regenerate it if exposed. <br>
Risk: The skill can publish, schedule, or cancel public Facebook Page posts. <br>
Mitigation: Require explicit human confirmation before publishing, scheduling, or canceling posts, and review the Page, content, media, and scheduled time before action. <br>
Risk: The security evidence notes a mismatch between the skill's posting behavior and one data-handling statement that says no content is uploaded or modified. <br>
Mitigation: Assume publishing workflows can upload media and modify public Page content, and review Boring permissions and data handling before use. <br>


## Reference(s): <br>
- [Boring MCP setup documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html) <br>
- [Boring API documentation](https://boring-doc.aiagent-me.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Text] <br>
**Output Format:** [Markdown guidance with structured MCP tool call parameters and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Boring MCP connector link with an embedded token for connected Facebook Pages.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
