## Description: <br>
Manage Facebook/Meta Ads -- create campaigns, ad sets, ads, monitor performance, and target audiences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and advertising operators use this skill to manage Meta Ads campaigns through AdAgent, including campaign setup, targeting research, ad creation, status changes, and performance review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live spend-affecting changes to Meta Ads campaigns, ad sets, ads, and budgets through an embedded MCP connector. <br>
Mitigation: Install only if AdAgent is trusted with Meta Ads account access, treat the MCP link like a password, verify connected Facebook permissions and ad accounts, and require explicit confirmation before creating, enabling, pausing, or changing budgets. <br>


## Reference(s): <br>
- [AdAgent](https://adagent.10xboost.org) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, API calls, configuration] <br>
**Output Format:** [Markdown guidance with tool-call instructions and tabular ad performance summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an MCP Connector link that contains embedded authentication for the AdAgent service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
