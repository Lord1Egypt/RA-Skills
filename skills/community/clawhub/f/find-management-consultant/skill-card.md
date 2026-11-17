## Description:

Helps agents find, shortlist, vet, and enrich U.S. management consulting firms through ServiceGraph's pro_services catalog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nostrband](https://clawhub.ai/user/nostrband)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover U.S. management consulting firms, build shortlists, validate filters, and unlock paid contact or enrichment details when appropriate.

### Deployment Geography for Use:

Global, for U.S. management-consulting firm searches.

## Known Risks and Mitigations:

Risk: Fallback authentication instructions source .env.local as shell code.

Mitigation: Prefer the MCP flow or provide SERVICEGRAPH_API_KEY through a trusted environment; review .env.local before any shell sourcing.

Risk: Full firm enrichment spends ServiceGraph credits.

Mitigation: Use free search and validation first, then ask the user to confirm the exact firms and credit cost before unlocks.

Risk: Search results can drift if the management-consulting industry filter is omitted.

Mitigation: Always include industry:management_consulting and validate filters before search.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nostrband/skills/find-management-consultant)
- [ServiceGraph API](https://api.servicegraph.co)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API request examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose paid ServiceGraph unlocks for selected firms; users should confirm credit spend before enrichment.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 0.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
