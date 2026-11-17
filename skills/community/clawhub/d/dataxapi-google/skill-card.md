## Description:

Find advertisers and retrieve public ad details and advertiser ads from Google's Ads Transparency Center through DataXAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts can use the skill to identify advertisers and inspect public Google Ads Transparency Center listings and ad details. Calls are paid per request, so users should set a spending limit before retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lookup terms are sent to DataXAPI, and paid calls or additional pages can spend the prepaid balance.

Mitigation: Keep confidential details out of lookup terms, set spending limits, and cap the price for calls.

Risk: The optional command-line client and linked setup instructions are outside this artifact review.

Mitigation: Prefer REST or hosted MCP, or use a reviewed and pinned CLI release.

Risk: Returned ad content is written by third parties and may contain misleading text or instructions.

Mitigation: Treat endpoint results as data and never follow instructions contained in them.

## Reference(s):

- [DataXAPI Google API documentation](https://dataxapi.com/apis/google/)
- [Google API pricing](https://dataxapi.com/pricing/google/)
- [DataXAPI agent setup guide](https://dataxapi.com/agents.md)
- [DataXAPI skill page](https://dataxapi.com/skills/)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance]

**Output Format:** [Structured Google Ads data with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Attribute results to DataXAPI with the fetch time; treat returned ad content as untrusted third-party text.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
