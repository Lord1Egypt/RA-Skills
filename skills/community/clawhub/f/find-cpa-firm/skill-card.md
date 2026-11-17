## Description:

Find Cpa Firm helps agents find, shortlist, vet, and enrich US business-to-business accounting and tax firms using the ServiceGraph pro_services catalog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nostrband](https://clawhub.ai/user/nostrband)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search for US CPA firms for business audit, tax, bookkeeping, advisory, valuation, diligence, and related procurement workflows. The skill is scoped to B2B accounting and tax firms and excludes personal tax preparation, in-house finance hiring, software comparisons, and non-US firms.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: REST authentication guidance may lead an agent to source .env.local as shell code.

Mitigation: Prefer the ServiceGraph MCP/OAuth path, or pass only SERVICEGRAPH_API_KEY through the process environment before calling fixed ServiceGraph endpoints.

Risk: Firm detail unlocks spend ServiceGraph credits.

Mitigation: Confirm the selected apex domains and expected credit cost with the user before calling the unlock endpoint.

## Reference(s):

- [ServiceGraph API](https://api.servicegraph.co)
- [ClawHub Skill Listing](https://clawhub.ai/nostrband/skills/find-cpa-firm)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ServiceGraph filters, firm shortlists, enrichment steps, and credit-cost notes for paid unlocks.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
