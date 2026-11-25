## Description:

Retrieves public WeChat Channels video, account, collection, and comment data through DataXAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve and summarize public WeChat Channels videos, account profiles, collections, comments, and engagement data through DataXAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Discovery queries may send user-provided words to DataXAPI.

Mitigation: Avoid including sensitive details in queries and review the information being sent before making a call.

Risk: The security scan says the skill may recommend running an unpinned package, and its review was partial.

Mitigation: Check the package source and version before running it, and review the referenced materials before installation.

## Reference(s):

- [DataXAPI](https://dataxapi.com)
- [DataXAPI agent setup instructions](https://dataxapi.com/agents.md)
- [WeChat Channels API reference](https://dataxapi.com/apis/wechat_channels/)
- [WeChat Channels API pricing](https://dataxapi.com/pricing/wechat_channels/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Guidance, Shell commands, Configuration instructions]

**Output Format:** [JSON API responses and concise text summaries, with optional Markdown, shell, or configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calls return one page at a time; paid endpoint calls are priced per call and support per-call price caps.]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
