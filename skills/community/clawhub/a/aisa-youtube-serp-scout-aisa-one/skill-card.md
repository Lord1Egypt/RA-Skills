## Description:

Search YouTube videos, channels, and trends through the AIsa YouTube SERP client for content research, competitor tracking, and trend discovery without managing Google credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and content researchers use this skill to search YouTube results, find top videos, and support competitor or trend research through the AIsa API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: YouTube research queries and the AISA_API_KEY are sent to api.aisa.one.

Mitigation: Use a dedicated, revocable, least-privilege AIsa key where possible, avoid sensitive query terms, and rotate the key if exposure is suspected.

Risk: Competitor and trend analysis may be misleading if treated as successful before the API returns usable data.

Mitigation: Check returned JSON for errors and result quality before summarizing findings or making recommendations.

## Reference(s):

- [AIsa homepage](https://aisa.one)
- [AIsa YouTube search endpoint](https://api.aisa.one/apis/v1/youtube/search)
- [ClawHub skill listing](https://clawhub.ai/aisadocs/skills/aisa-youtube-serp-scout-aisa-one)
- [AIsa publisher profile](https://clawhub.ai/user/aisadocs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; requests are sent to api.aisa.one.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
