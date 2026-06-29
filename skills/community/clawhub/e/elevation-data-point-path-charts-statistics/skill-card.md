## Description: <br>
Provides AgentPMT-hosted elevation lookups for points and paths, including elevation units, path statistics, and optional elevation profile chart URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to request elevation data for individual coordinates or route paths for trail planning, cycling route assessment, surveying, flood-risk mapping, real estate site review, and terrain visualization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location coordinates and route points are sent to AgentPMT for elevation lookup. <br>
Mitigation: Send only the coordinates needed for the task and avoid including unrelated sensitive location context. <br>
Risk: Generated elevation chart images may be accessible through signed URLs for 7 days. <br>
Mitigation: Share chart URLs only with intended recipients and avoid generating charts for routes that should not be exposed. <br>
Risk: AgentPMT calls consume credits, and higher sample counts can increase usage. <br>
Mitigation: Confirm the account route and choose sample counts appropriate to the analysis before making repeated or high-volume calls. <br>
Risk: Account secrets, wallet material, signatures, or payment headers could be exposed if placed in prompts or logs. <br>
Mitigation: Use the setup skill for credential handling and keep secrets out of prompts, chat transcripts, and logs. <br>


## Reference(s): <br>
- [Action schema](artifact/schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/elevation-data-point-path-charts-statistics) <br>
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/elevation-data-point-path-charts-statistics) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown instructions with JSON request examples and schema references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote AgentPMT calls return JSON elevation data, statistics, and optional PNG chart signed URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
