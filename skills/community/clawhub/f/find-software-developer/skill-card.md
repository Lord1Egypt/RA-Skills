## Description:

Helps agents find, shortlist, vet, and enrich US software development firms by mapping user requests to ServiceGraph pro_services searches and enrichment workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nostrband](https://clawhub.ai/user/nostrband)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover and compare US software development vendors for custom software, web, mobile, backend/API, DevOps/cloud, systems integration, and hosting-related needs. It helps convert informal requirements into ServiceGraph filters, shortlist firms, and manage paid detail unlocks with user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The REST authentication guidance includes a shell pattern that sources .env.local, which can execute local file contents.

Mitigation: Use a pre-exported SERVICEGRAPH_API_KEY or a safe secret manager or MCP integration instead of sourcing .env.local.

Risk: Firm-detail unlocks can spend ServiceGraph credits.

Mitigation: Confirm the selected firms and expected credit cost with the user before calling the unlock endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nostrband/skills/find-software-developer)
- [ServiceGraph API](https://api.servicegraph.co)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration, Guidance]

**Output Format:** [Markdown with API request examples, shell commands, and shortlist guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require SERVICEGRAPH_API_KEY for authenticated API calls and user confirmation before paid firm-detail unlocks.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter: 0.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
