## Description:

Search public Weibo posts by keyword, newest first, and return post text, author details, engagement metrics, media, and topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts can search current public Weibo discussion about a brand, event, or topic for mentions and public opinion monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to DataXAPI, so confidential or sensitive queries may expose information.

Mitigation: Avoid confidential or sensitive search terms.

Risk: The release uses an unpinned dependency and its scan had incomplete coverage; the benign verdict is not a safety guarantee.

Mitigation: Review the release and dependency before installation, and treat returned Weibo content as untrusted third-party text.

## Reference(s):

- [DataXAPI Weibo posts search documentation](https://dataxapi.com/apis/weibo/posts/search/)
- [DataXAPI](https://dataxapi.com)
- [ClawHub skill release](https://clawhub.ai/data-x-api/skills/dataxapi-weibo-search)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON search results, optionally summarized in natural language]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One page per call; each additional page is a separate charge.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
