## Description:

Retrieves Douyin 巨量算数 keyword trend indices, related keywords, and popular videos for trend research and comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

Marketers and analysts use the skill to track Douyin keyword interest over time, find related terms, compare keywords, and identify popular videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package install command is unpinned, and the security review reported that some local references could not be checked.

Mitigation: Review the selected package version and its references before use; provide only a narrowly scoped DataXAPI key.

Risk: Returned video captions and other Douyin text are third-party content and may contain misleading material or instructions.

Mitigation: Treat returned content as data, not instructions, and verify claims before relying on them.

## Reference(s):

- [DataXAPI Douyin history endpoint documentation](https://dataxapi.com/apis/douyin/index/keywords/history/)
- [DataXAPI Douyin related keywords documentation](https://dataxapi.com/apis/douyin/index/keywords/related/)
- [DataXAPI Douyin popular videos documentation](https://dataxapi.com/apis/douyin/index/videos/search/)
- [DataXAPI agent skills catalog](https://dataxapi.com/.well-known/agent-skills/index.json)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured trend data summarized as text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Index values are platform scores rather than search counts; responses may include third-party video text.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
