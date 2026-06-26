## Description: <br>
Publish posts to Facebook Pages using Boring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and social media operators use this skill to publish, schedule, view, and cancel Facebook Page posts through Boring after connecting a Facebook Page and adding the MCP connector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP connector URL contains an embedded authentication token that can publish or schedule public Facebook Page posts if exposed. <br>
Mitigation: Keep the connector URL private, regenerate it if exposed, and connect only intended Facebook Pages. <br>
Risk: Publishing, scheduling, or canceling posts can change public Facebook Page content. <br>
Mitigation: Require explicit user confirmation before publish, schedule, or cancel operations. <br>


## Reference(s): <br>
- [Boring MCP setup guide](https://boring-doc.aiagent-me.com/getting-started/mcp.html) <br>
- [Boring documentation](https://boring-doc.aiagent-me.com) <br>
- [ClawHub skill page](https://clawhub.ai/snoopyrain/boring-facebook-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Guidance, Markdown] <br>
**Output Format:** [Markdown with MCP tool call parameters and publishing status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before publishing, scheduling, or canceling posts; uses a private MCP connector URL with embedded authentication.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
