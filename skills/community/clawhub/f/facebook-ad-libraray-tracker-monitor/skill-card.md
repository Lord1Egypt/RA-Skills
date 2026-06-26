## Description: <br>
Monitor Facebook ads and advertisers with PPSPY, including tracking tasks, ad activity trends, landing pages, products, and monitoring groups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanyanggod](https://clawhub.ai/user/fanyanggod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and marketing analysts use this skill to monitor Facebook advertisers, create and manage PPSPY tracking tasks, and review ad, landing-page, and product performance over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and uses a third-party MCP server. <br>
Mitigation: Confirm that PPSPY and the ppspy-mcp-server npm package are trusted before installation. <br>
Risk: The skill uses a PPSPY API key and can consume monitoring quota or modify monitoring groups and tasks. <br>
Mitigation: Use an API key with acceptable billing and quota limits, and review monitoring task or group changes before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fanyanggod/facebook-ad-libraray-tracker-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/fanyanggod) <br>
- [PPSPY homepage](https://www.ppspy.com) <br>
- [PPSPY API site](https://api.ppspy.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown and structured MCP tool-call results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a PPSPY API key and the ppspy-mcp-server npm package.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
