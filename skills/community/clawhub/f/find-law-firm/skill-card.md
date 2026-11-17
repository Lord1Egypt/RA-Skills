## Description:

Finds, shortlists, vets, and enriches US business-to-business law firms across corporate practice areas using the ServiceGraph pro_services catalog, while excluding consumer legal matters, non-US firms, in-house hires, freelancers, and DIY legal research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nostrband](https://clawhub.ai/user/nostrband)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to procure and compare US B2B law firms by practice area, location, size, ratings, and domain. It is intended for business legal-service discovery and enrichment, not personal legal advice or consumer legal referrals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The REST fallback auth recipe can execute `.env.local` as shell code while loading credentials.

Mitigation: Prefer the ServiceGraph MCP/OAuth path, or pass only SERVICEGRAPH_API_KEY through safer secret handling or a non-executing dotenv parser.

Risk: Detail enrichment sends law-firm lookup requests to ServiceGraph and can spend credits on paid unlocks.

Mitigation: Show the selected firm apexes and credit cost before unlocking, require explicit user choice, and avoid sending unrelated user data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nostrband/skills/find-law-firm)
- [ServiceGraph API](https://api.servicegraph.co)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API request examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce ServiceGraph API queries and should require explicit user approval before paid firm-detail unlocks.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter declares 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
