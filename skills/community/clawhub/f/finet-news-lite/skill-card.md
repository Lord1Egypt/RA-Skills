## Description:

Fetches recent Finet financial news and returns normalized article records with built-in request timeouts and retries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finet8317](https://clawhub.ai/user/finet8317)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve recent Finet financial news as consistent article records for news monitoring and processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changing FINET_API_HOST redirects outbound news requests to another host.

Mitigation: Leave FINET_API_HOST unset unless you trust the replacement host.

## Reference(s):

- [finet-news-lite on ClawHub](https://clawhub.ai/finet8317/skills/finet-news-lite)
- [Finet recent-news data source](https://cps.finet.com.cn/cps_api/news/recent-list)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [JSON array of normalized article records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live, uncached results; article content may contain HTML.]

## Skill Version(s):

1.0.1 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
