## Description:

Compare user-supplied candidate locations for a local business using nearby competitors, public access signals, review samples, and available city-level context. Use for an early screen, not a lease or viability recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Small-business owners, planners, and advisors use this skill to compare a fixed set of user-supplied candidate locations using competitor, access, review, and city-level context. It supports early screening and follow-up research, not a lease or site-viability decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends requests and an API key to api.crawlora.net, and candidate coordinates or route anchors may be shared with mapping providers.

Mitigation: Use public or general locations for screening; before submitting a home address, unpublished site, or confidential expansion location, explain the data sharing and get explicit consent. Use the Crawlora service only if you trust it with the API key.

## Reference(s):

- [Endpoint reference](reference/endpoints.md)
- [ClawHub release page](https://clawhub.ai/crawlora-org/skills/business-location-screening)
- [Crawlora API key signup](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown candidate-by-candidate evidence matrix]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source coverage, retrieval times, and missing inputs where available.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
