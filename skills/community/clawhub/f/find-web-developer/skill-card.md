## Description:

Finds, shortlists, vets, and enriches US web development firms for website builds, refreshes, ecommerce, landing pages, CMS projects, and frontend web work using the ServiceGraph pro_services catalog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nostrband](https://clawhub.ai/user/nostrband)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to identify US web development agencies, filter by platform, location, vertical, ratings, and other project needs, and enrich selected firms after confirming credit usage.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: REST authentication guidance can execute a local .env.local file as shell code.

Mitigation: Prefer the ServiceGraph MCP/OAuth path or read SERVICEGRAPH_API_KEY from a trusted existing environment; do not source .env.local from an untrusted repository or project directory.

Risk: Unlocking firm details spends ServiceGraph credits.

Mitigation: Confirm selected firms and credit cost with the user before calling paid unlock endpoints.

## Reference(s):

- [Find Web Developer on ClawHub](https://clawhub.ai/nostrband/skills/find-web-developer)
- [ServiceGraph API](https://api.servicegraph.co)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ServiceGraph filters, firm shortlists, unlock-cost prompts, and enrichment guidance.]

## Skill Version(s):

1.0.0 (source: release evidence; artifact frontmatter reports 0.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
