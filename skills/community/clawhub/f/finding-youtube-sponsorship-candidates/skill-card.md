## Description:

Finds YouTube channels suitable for brand sponsorships using apidojo's YouTube scraper on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External brand partnerships managers, sponsorship agencies, and SaaS marketing teams use this skill to discover and rank YouTube channels for sponsorship outreach in a target niche.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sponsorship research queries and YouTube targets are sent to Apify.

Mitigation: Use only data that is appropriate for a third-party Apify workflow and avoid including confidential campaign details in research queries.

Risk: The documented REST fallback passes the Apify token in the request URL.

Mitigation: Prefer a trusted MCP integration or a runner that uses an Authorization header or secret manager.

Risk: The artifact references a local scripts/run_actor.js helper that is not bundled with the release evidence.

Mitigation: Review and trust the local runner before executing it, or use the Apify MCP path instead.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-youtube-sponsorship-candidates)
- [Publisher profile](https://clawhub.ai/user/apidojo-io)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with ranked tables, plus optional CSV or JSON saved files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranks channels into TIER A, TIER B, and TIER C using subscriber count, average views, engagement, niche fit, sponsorship history, and score.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact metadata version 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
