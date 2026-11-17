## Description:

Finds brand ambassador candidates on Instagram and TikTok using apidojo's scrapers on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Brand partnership managers, DTC brands, and ambassador program coordinators use this skill to find creators who already mention a brand or related product category organically, then rank them for ambassador outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Instagram and TikTok data is processed through Apify actors.

Mitigation: Install only when this external processing is acceptable for the intended brand and audience data.

Risk: The artifact documents a query-string token fallback for the Apify API.

Mitigation: Use a least-privilege Apify token and prefer Authorization header handling over token values in URLs.

Risk: The optional customMapFunction parameter can introduce a JavaScript execution surface in the Apify actor workflow.

Mitigation: Avoid customMapFunction unless the execution behavior is understood and the function has been reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/apidojo-io/skills/finding-brand-ambassador-candidates)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown with ranked tables, scoring notes, and inline shell/API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces creator handles, mention frequency, engagement rate, follower counts, competing sponsor signals, affinity signals, and tiered ambassador recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
