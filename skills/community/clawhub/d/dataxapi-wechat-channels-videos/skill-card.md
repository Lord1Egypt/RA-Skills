## Description:

Search WeChat Channels videos by topic, retrieve a video's details, and find accounts or list their videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users can search WeChat Channels videos by keyword, inspect a video's metrics and file, find accounts by exact name, and list an account's videos through DataXAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends an unpinned package, which raises a supply-chain concern.

Mitigation: Review the package source and select a pinned version before installation when available.

Risk: Search terms or lookup identifiers may be sent to DataXAPI.

Mitigation: Avoid sending sensitive terms or identifiers, and review the data provider's terms before making calls.

Risk: The security analysis is incomplete because some local path-like references could not be resolved.

Mitigation: Review unresolved references and the package contents before installation.

## Reference(s):

- [DataXAPI homepage](https://dataxapi.com)
- [WeChat Channels video search API](https://dataxapi.com/apis/wechat_channels/videos/search/)
- [WeChat Channels video details API](https://dataxapi.com/apis/wechat_channels/videos/get/)
- [WeChat Channels account video list API](https://dataxapi.com/apis/wechat_channels/users/videos/list/)
- [WeChat Channels account search API](https://dataxapi.com/apis/wechat_channels/users/search/)

## Skill Output:

**Output Type(s):** [JSON data, Text]

**Output Format:** [Structured video and account records with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include video and account details, engagement figures, links, and expiring video file access information.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
