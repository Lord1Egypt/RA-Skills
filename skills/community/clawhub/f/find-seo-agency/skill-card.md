## Description:

Find Seo Agency helps agents find, shortlist, vet, and enrich US SEO agencies through the ServiceGraph pro_services dataset.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nostrband](https://clawhub.ai/user/nostrband)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to ask an agent for US SEO agency shortlists, vetting, and contact enrichment while keeping searches constrained to SEO services in the ServiceGraph pro_services dataset.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sourcing .env.local as shell code can execute local shell content while loading credentials.

Mitigation: Use the ServiceGraph MCP server or a harness-injected SERVICEGRAPH_API_KEY; do not have the agent source .env.local directly.

Risk: Paid unlock calls spend credits for each selected firm.

Mitigation: Show the selected apex domains and total credit cost, then get explicit user confirmation before calling POST /unlocks.

Risk: The skill depends on an external API and credentialed requests.

Mitigation: Keep API keys out of chat and model context, and send only the search criteria needed for the user's agency search.

## Reference(s):

- [Find Seo Agency ClawHub listing](https://clawhub.ai/nostrband/skills/find-seo-agency)
- [ServiceGraph API](https://api.servicegraph.co)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline curl examples and API request patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require SERVICEGRAPH_API_KEY and user confirmation before paid unlocks.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
