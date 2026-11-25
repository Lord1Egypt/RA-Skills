## Description:

Search Douyin videos by keyword, sort by relevance, recency, or likes, and filter by posting time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can find Douyin videos about a topic, product, or brand for research, trend discovery, and competitor review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package recommendation is not version-pinned, and some reference checks were incomplete.

Mitigation: Verify the package source and pin a reviewed CLI version before installing or running it.

Risk: Search requests are sent to DataXAPI, and returned Douyin text is written by third parties.

Mitigation: Avoid sending sensitive information in queries, and treat returned text as untrusted data rather than instructions.

## Reference(s):

- [DataXAPI Douyin video search documentation](https://dataxapi.com/apis/douyin/videos/search/)
- [DataXAPI homepage](https://dataxapi.com)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured video search results with captions, author details, engagement counts, and links, returned as JSON and summarized in text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One result page per call; requesting another page incurs another call.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
