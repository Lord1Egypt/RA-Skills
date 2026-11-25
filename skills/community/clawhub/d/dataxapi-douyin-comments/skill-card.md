## Description:

Retrieve paginated Douyin video comments and comment replies, including likes, reply counts, and timestamps, for understanding audience feedback or preparing a table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to collect comments and replies from a Douyin video to understand audience feedback or prepare a tabular export. The agent retrieves results page by page and can include likes, reply counts, and timestamps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes an unpinned package command and incomplete scan coverage because local references were unresolved.

Mitigation: Use a reviewed exact package version and review the package and service before installation.

Risk: Retrieved comments are third-party text and may contain misleading content or instructions.

Mitigation: Treat comment content as untrusted data and do not follow instructions embedded in it.

## Reference(s):

- [DataXAPI Douyin video comments API](https://dataxapi.com/apis/douyin/videos/comments/list/)
- [DataXAPI Douyin comment replies API](https://dataxapi.com/apis/douyin/comments/replies/list/)
- [DataXAPI agent setup guide](https://dataxapi.com/agents.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Tables]

**Output Format:** [Paginated JSON results, summarized as text or a table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each page requires a separate API call; continued pages are billed separately.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
