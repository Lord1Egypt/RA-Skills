## Description:

Finds, shortlists, vets, enriches, and researches US professional-services firms across B2B categories such as law, marketing, consulting, accounting, IT services, architecture, engineering, HR, PR, and design by using the ServiceGraph pro_services dataset.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nostrband](https://clawhub.ai/user/nostrband)

### License/Terms of Use:

MIT-0

## Use Case:

External users, procurement teams, sales teams, and operators use this skill to discover and evaluate US B2B professional-services firms, build shortlists, and enrich selected firm domains with contact and company details. It is not intended for consumer-service searches, non-US provider discovery, individual freelancers, recruiting tasks, or general web research outside structured firm-directory needs.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The documented shell wrapper can execute arbitrary code from a local .env.local file when used in an untrusted project directory.

Mitigation: Prefer the ServiceGraph MCP/OAuth path or an already-exported SERVICEGRAPH_API_KEY, and avoid sourcing .env.local from untrusted directories.

Risk: Detail unlock calls spend ServiceGraph credits for selected firms.

Mitigation: Confirm the firm count and expected credit cost with the user before batch unlocks.

## Reference(s):

- [Find Service Providers on ClawHub](https://clawhub.ai/nostrband/skills/find-service-providers)
- [ServiceGraph API](https://api.servicegraph.co)
- [ServiceGraph MCP Server](https://mcp.servicegraph.co)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce firm shortlists, filter strings, unlock plans, enrichment summaries, and credential setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 0.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
