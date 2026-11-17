## Description:

Find Marketing Agency helps an agent find, shortlist, vet, and enrich US marketing agencies using the ServiceGraph pro_services catalog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nostrband](https://clawhub.ai/user/nostrband)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business teams use this skill to discover, compare, and enrich US marketing agencies by service area, location, size, ratings, and third-party listing signals. It is intended for agency shortlisting and contact enrichment, not for SEO-only searches, web development searches, recruiting in-house marketers, or non-US provider discovery.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The REST fallback can source a workspace .env.local file, which may execute shell code controlled by the workspace.

Mitigation: Prefer the MCP/OAuth path. If REST is used, provide SERVICEGRAPH_API_KEY through a trusted environment or secret manager instead of sourcing .env.local.

Risk: Unlock requests spend ServiceGraph credits for firm details.

Mitigation: Confirm the selected firms and total credit cost with the user before submitting paid unlock calls.

## Reference(s):

- [ServiceGraph API](https://api.servicegraph.co)
- [ClawHub Skill Page](https://clawhub.ai/nostrband/skills/find-marketing-agency)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API request examples and shortlist or enrichment results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide authenticated API calls and paid unlock decisions; user approval should precede credit-spending unlock requests.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter version is 0.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
