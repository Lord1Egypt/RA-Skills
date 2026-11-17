## Description:

Retrieves public Meta Ad Library ads and advertiser information through DataXAPI, including search results, ad details, advertiser listings, and video transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to search public Meta ads, look up ads or advertisers by name, ID, or link, and retrieve video transcripts when those details answer a user's question.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API requests and additional result pages can incur charges, and search terms or ad identifiers are sent to DataXAPI.

Mitigation: Use a scoped key with a budget limit, leave confidential details out of search terms, check prices before multi-page requests, and cap spending with the documented maximum-price option.

Risk: The optional command-line package and returned third-party ad content may be unsafe to trust blindly.

Mitigation: Review and pin the CLI package before running it, and treat returned ad content as data rather than instructions.

## Reference(s):

- [DataXAPI Skills](https://dataxapi.com/skills/)
- [Meta Ad Library API documentation](https://dataxapi.com/apis/meta/)
- [Meta API pricing](https://dataxapi.com/pricing/meta/)
- [DataXAPI agent setup](https://dataxapi.com/agents.md)

## Skill Output:

**Output Type(s):** [Text, Structured data, Guidance]

**Output Format:** [DataXAPI result data and concise Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can contain ad text, advertiser details, media information, and video transcripts; retrieving additional pages can incur additional charges.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
