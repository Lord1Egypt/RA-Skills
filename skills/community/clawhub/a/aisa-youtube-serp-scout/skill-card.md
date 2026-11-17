## Description:

Search YouTube videos, channels, and trends through the AIsa YouTube SERP client for content research, competitor tracking, and trend discovery without managing Google credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

Content researchers, marketers, and developers use this skill to query YouTube search results, monitor trends, identify top videos, and research competitor channel presence through the AIsa API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: YouTube search queries, filter tokens, and authenticated API usage are sent to api.aisa.one.

Mitigation: Use the skill only where AIsa is an approved service provider, and avoid sensitive private research terms unless that data sharing is acceptable.

Risk: The skill depends on an AISA_API_KEY for API access.

Mitigation: Store the key in the runtime environment, restrict access to trusted users, and rotate it if exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bibaofeng/skills/aisa-youtube-serp-scout)
- [AIsa Homepage](https://aisa.one)
- [AIsa YouTube Search Endpoint](https://api.aisa.one/apis/v1/youtube/search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and sends YouTube search parameters to api.aisa.one.]

## Skill Version(s):

1.0.2 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
