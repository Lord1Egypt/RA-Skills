## Description:

Retrieves public Douyin videos, accounts, comments, trends, keyword indexes, and Xingtu creator data through DataXAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to look up public Douyin content and creator or account trends from a query, Douyin link, ID, or account name.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Douyin search terms are sent to DataXAPI.

Mitigation: Avoid including private context in search terms and review the provider's data handling before making calls.

Risk: Installation commands do not pin a package version, and scan coverage was partial because local references could not be resolved.

Mitigation: Review the package version and unresolved references before installation.

## Reference(s):

- [DataXAPI Douyin API catalog](https://dataxapi.com/apis/douyin/)
- [DataXAPI Douyin pricing](https://dataxapi.com/pricing/douyin/)
- [DataXAPI agent setup](https://dataxapi.com/agents.md)
- [DataXAPI homepage](https://dataxapi.com)
- [ClawHub skill release](https://clawhub.ai/data-x-api/skills/dataxapi-douyin)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured API response data with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One API response page per call; each additional page is a separately billed call.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
