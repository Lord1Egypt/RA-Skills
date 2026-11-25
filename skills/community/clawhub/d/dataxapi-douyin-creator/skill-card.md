## Description:

Find Douyin accounts by keyword, read creator profiles, and list their videos with engagement figures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users can find Douyin creators by keyword, inspect account statistics, and review a creator's recent videos and engagement figures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The suggested dataxapi package version is unpinned, which the security evidence identifies as a supply-chain risk.

Mitigation: Review the package source and pin a trusted version before installation.

Risk: The skill relies on the DataXAPI service, and the security guidance calls out trust in that service and package source.

Mitigation: Use the service only with an API key appropriate for the account and review each call's price before making paid requests.

Risk: The security scan was marked partial because some local references could not be resolved, leaving incomplete evidence.

Mitigation: Resolve and review the outstanding references, then repeat the security scan before relying on the result.

## Reference(s):

- [DataXAPI](https://dataxapi.com)
- [Douyin account search API](https://dataxapi.com/apis/douyin/users/search/)
- [Douyin creator profile API](https://dataxapi.com/apis/douyin/users/get/)
- [Douyin creator videos API](https://dataxapi.com/apis/douyin/users/videos/list/)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Creator and video data summarized as text or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paged results; available fields vary by endpoint.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
