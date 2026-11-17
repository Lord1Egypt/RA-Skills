## Description:

Finds, shortlists, vets, and enriches U.S. design and creative agencies through the ServiceGraph pro_services dataset, with filters for services, location, size, ratings, and related design disciplines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nostrband](https://clawhub.ai/user/nostrband)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill for B2B procurement workflows that identify suitable U.S. design and creative agencies, including UX/UI, branding, product design, packaging, graphic design, and contact enrichment.

### Deployment Geography for Use:

Global, for searches constrained to U.S. firms.

## Known Risks and Mitigations:

Risk: The fallback authentication example sources .env.local as shell code while handling an API key.

Mitigation: Prefer the ServiceGraph MCP/OAuth path or export only SERVICEGRAPH_API_KEY through a trusted secret mechanism; do not source arbitrary .env.local files from untrusted projects.

Risk: Full firm details require paid unlocks using ServiceGraph credits.

Mitigation: Use free search and brief reads first, then confirm the number of firms and credit cost before unlocking detail records.

## Reference(s):

- [Find Design Agency on ClawHub](https://clawhub.ai/nostrband/skills/find-design-agency)
- [ServiceGraph API](https://api.servicegraph.co)
- [ServiceGraph pro_services Fields Endpoint](https://api.servicegraph.co/v1/datasets/pro_services/fields)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, API calls]

**Output Format:** [Markdown with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and brief lookup are free; detail unlocks cost credits and last 30 days.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
