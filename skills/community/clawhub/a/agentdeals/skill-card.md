## Description: <br>
Search and compare 1,500+ developer infrastructure deals: free tiers, startup credits, and pricing changes across 54 categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robhunter](https://clawhub.ai/user/robhunter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agents use AgentDeals to find free tiers and startup credits, compare vendors, plan or audit infrastructure stacks, and monitor pricing changes before choosing developer services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vendor searches, stack audits, use cases, client details, and session identifiers may be sent to the hosted service, logged, and exposed through public telemetry endpoints. <br>
Mitigation: Avoid confidential stack plans or internal vendor evaluations; use sanitized queries until telemetry endpoints are gated and minimization, retention, and privacy disclosures are corrected. <br>
Risk: Users may over-trust read-only deal recommendations while the security evidence flags under-disclosed telemetry. <br>
Mitigation: Review the security summary before installation and treat outputs as public-service lookups unless the publisher updates privacy controls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/robhunter/agentdeals) <br>
- [AgentDeals Homepage](https://agentdeals.dev) <br>
- [AgentDeals API Documentation](https://agentdeals.dev/api/docs) <br>
- [AgentDeals MCP Endpoint](https://agentdeals.dev/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown or plain text summaries with MCP tool outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only deal lookup, vendor comparison, stack planning, and pricing-change tracking results.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
