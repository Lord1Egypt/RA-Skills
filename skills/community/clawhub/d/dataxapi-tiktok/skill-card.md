## Description:

Fetch public TikTok video, hashtag, user, comment, advertising, Creative Center, and TikTok Shop data through DataXAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve public TikTok videos, account details, comments, hashtags, ads, transcripts, and US TikTok Shop listings, then answer questions with the returned data.

### Deployment Geography for Use:

Global; TikTok Shop endpoints cover the United States.

## Known Risks and Mitigations:

Risk: The security assessment reports a version-unpinned package installation and execution path, and scan coverage was partial because some local path-like references were unresolved.

Mitigation: Review and pin the package version before installation, and inspect the unresolved references before relying on the scan as complete.

## Reference(s):

- [DataXAPI TikTok API documentation](https://dataxapi.com/apis/tiktok/)
- [DataXAPI TikTok pricing](https://dataxapi.com/pricing/tiktok/)
- [DataXAPI agent setup guide](https://dataxapi.com/agents.md)
- [DataXAPI homepage](https://dataxapi.com)
- [ClawHub skill release](https://clawhub.ai/data-x-api/skills/dataxapi-tiktok)

## Skill Output:

**Output Type(s):** [JSON, Text, Analysis]

**Output Format:** [Structured TikTok data with concise natural-language answers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API calls are billed per page; additional pages incur additional charges.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
