## Description:

Find, shortlist, vet, and enrich US recruiting and staffing firms through the ServiceGraph pro_services API, including executive search, RPO, contingent staffing, temp staffing, and vertical recruiting specialties.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nostrband](https://clawhub.ai/user/nostrband)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and sourcing teams use this skill to procure external US recruiting or staffing firms and to enrich firm records before deciding whether to spend credits on detailed contact data. It is not intended for job-board advice, hiring in-house recruiters, candidate-side job search help, career coaching, non-US firm searches, or individual freelance recruiters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents sourcing .env.local as shell code for REST authentication, which the authoritative security summary identifies as an avoidable high-impact risk.

Mitigation: Prefer the MCP/OAuth path, a trusted secret manager, or a pre-set SERVICEGRAPH_API_KEY environment variable; avoid sourcing local environment files unless the workspace contents are trusted.

Risk: Detailed firm unlocks spend ServiceGraph credits.

Mitigation: Confirm the number of firms, total credit cost, and whether cached 30-day access applies before running unlock operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nostrband/skills/find-recruiting-firm)
- [ServiceGraph API Base](https://api.servicegraph.co)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, API calls, configuration]

**Output Format:** [Markdown with inline shell commands, API request examples, and concise firm shortlist guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose free search, validation, and brief-read calls; detailed firm unlocks cost credits and require user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
