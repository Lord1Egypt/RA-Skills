## Description: <br>
Manage Google Ads campaigns by creating, monitoring, pausing, and optimizing search ads through AdAgent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Google Ads account owners and marketing operators use this skill to inspect accounts, research keywords, create paused search campaigns, review performance, and pause or enable campaigns through an AdAgent MCP connector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect ad spend and campaign delivery by creating campaigns, changing budgets, enabling campaigns, or pausing active campaigns. <br>
Mitigation: Require explicit user confirmation before any campaign creation, budget change, enablement, or pause action. <br>
Risk: The MCP connector link contains embedded authorization material and should be treated as a credential. <br>
Mitigation: Store the connector link like a password, avoid sharing it publicly, and rotate or reconnect access if it may have been exposed. <br>
Risk: The skill depends on a third-party AdAgent service with Google Ads OAuth access. <br>
Mitigation: Install and use it only if the operator trusts AdAgent with the connected Google Ads accounts and reviews account access before use. <br>


## Reference(s): <br>
- [AdAgent homepage](https://adagent.10xboost.org) <br>
- [ClawHub skill page](https://clawhub.ai/snoopyrain/adagent-google-ads) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/snoopyrain) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with MCP connector setup steps, tool-call examples, and tabular campaign or performance results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct AdAgent MCP operations that read Google Ads data or change campaign state after connector configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
