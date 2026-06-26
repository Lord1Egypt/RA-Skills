## Description: <br>
Find, shortlist, vet, enrich, and research US B2B professional-services firms using the ServiceGraph pro_services dataset and API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nostrband](https://clawhub.ai/user/nostrband) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external procurement teams, developers, and agents use this skill to search and enrich US-based B2B service providers such as law firms, agencies, consultancies, accounting firms, IT services firms, and similar vendors. It is intended for structured firm discovery and shortlist workflows, not consumer-service requests, non-US firms, freelancers, recruiting tasks, or general web research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan flags credential-loading instructions that can source local .env.local shell code. <br>
Mitigation: Prefer the ServiceGraph MCP/OAuth flow or an already-exported SERVICEGRAPH_API_KEY, and do not source .env.local unless the user explicitly trusts that file. <br>
Risk: The skill can trigger paid ServiceGraph unlocks for firm details. <br>
Mitigation: Confirm the number of firms and expected credit cost with the user before running unlock calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nostrband/find-service-providers) <br>
- [ServiceGraph API base](https://api.servicegraph.co) <br>
- [ServiceGraph MCP server](https://mcp.servicegraph.co) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with API request examples and structured shortlist guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ServiceGraph filters, API calls, shortlist summaries, enrichment planning, and cost/credit guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter: 0.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
