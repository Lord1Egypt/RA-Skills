## Description:

Find Pr Agency helps agents find, shortlist, vet, and enrich US public-relations and communications agencies through ServiceGraph's pro_services dataset.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nostrband](https://clawhub.ai/user/nostrband)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to identify US PR and communications agencies for media relations, crisis communications, investor relations, product launches, public affairs, brand reputation, internal communications, or enrichment of known PR firm domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback authentication flow may execute a local .env file as shell code.

Mitigation: Prefer the ServiceGraph MCP/OAuth path or require SERVICEGRAPH_API_KEY to already be present in the process environment; do not let the agent source .env.local.

Risk: Sensitive business intent, such as fundraising, IPO, crisis, legal, regulatory, healthcare, or unreleased launch details, may be sent to a third-party API.

Mitigation: Have the agent build filters locally or confirm the minimized text before sending requests to ServiceGraph.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nostrband/skills/find-pr-agency)
- [ServiceGraph API](https://api.servicegraph.co)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Markdown guidance with ServiceGraph API request examples, filter DSL snippets, shortlist recommendations, and enrichment steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include credit-cost notes for paid firm-detail unlocks and reminders to keep API keys out of chat.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter declares 0.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
