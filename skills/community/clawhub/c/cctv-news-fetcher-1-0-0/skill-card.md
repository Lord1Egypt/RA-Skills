## Description:

Fetch and parse news highlights from CCTV News Broadcast (Xinwen Lianbo) for a given date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pppig1357](https://clawhub.ai/user/pppig1357)

### License/Terms of Use:

MIT-0

## Use Case:

External users or agents use this skill to retrieve CCTV News Broadcast highlights for a specific date and summarize the fetched titles and article content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler makes outbound web requests and can follow links discovered from remote CCTV pages.

Mitigation: Run in a controlled network environment and allowlist expected CCTV domains before deployment.

Risk: The crawler lacks explicit date validation, request timeouts, and response size limits.

Mitigation: Validate dates before execution and add operational limits for network requests and parsed responses.

Risk: The crawler sends fixed Cookie and Host headers that may be unnecessary for normal use.

Mitigation: Review and remove unnecessary headers unless they are required for the intended deployment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/pppig1357/skills/cctv-news-fetcher-1-0-0)
- [CCTV News Broadcast daily archive](https://tv.cctv.com/lm/xwlb/day/)
- [CCTV News Broadcast legacy archive](https://cctv.cntv.cn/lm/xinwenlianbo/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [JSON crawler output with a text or markdown summary for the user]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a date in YYYYMMDD format when a specific day is requested.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
