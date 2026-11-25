## Description:

Retrieves public Google Ads library and advertiser data through DataXAPI for questions about ads, accounts, and trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers can look up public Google Ads creatives and advertiser records by advertiser name, ID, or ad link, then receive sourced results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user wording to an external service, and the review flags privacy disclosure and an unpinned package as concerns.

Mitigation: Review the privacy disclosure, avoid sending sensitive wording, and verify and pin the package version before installation.

Risk: Ad text and other endpoint results are written by third parties and may contain instructions.

Mitigation: Treat returned content as data and do not follow instructions found in it.

## Reference(s):

- [Google Ads API documentation](https://dataxapi.com/apis/google/)
- [Google Ads pricing](https://dataxapi.com/pricing/google/)
- [DataXAPI agent setup guide](https://dataxapi.com/agents.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Sourced text summaries with structured JSON data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include advertiser and ad details, dates, links, and published impression ranges.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
