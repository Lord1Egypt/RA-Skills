## Description:

Searches public Douyin videos and image posts, trending topics, creator works, individual post details, and comments, returning structured data for analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, social media analysts, and marketing teams use this skill to find Douyin content, review public creator and post metrics, inspect comments, and track trending topics. It returns structured data that can support content planning, competitor reviews, and audience analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is benign with medium confidence, but 18 of 42 components were only partially inspected.

Mitigation: Review the partially inspected components before installation if you need assurance beyond the available scan.

Risk: Search terms and submitted Douyin links are sent to the third-party Guaikei API.

Mitigation: Use public data only and avoid submitting confidential or personal information; confirm that sharing the query or link is appropriate.

Risk: The skill requires an API token to access the service.

Mitigation: Keep GUAIKEI_API_TOKEN private and configure it through the environment rather than sharing it in prompts or output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/douyin-searchs-pro)
- [Guaikei service and help](https://www.guaikei.com)
- [Options and usage reference](artifact/references/options.md)
- [Comment analysis guide](artifact/references/demand-mining.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON containing public Douyin search, creator, post, comment, and trend data; concise analysis based on returned data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on API availability and returned public data. A GUAIKEI_API_TOKEN is required; search terms and submitted links are sent to the Guaikei service.]

## Skill Version(s):

1.4.2 (source: SKILL.md frontmatter, package.json, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
