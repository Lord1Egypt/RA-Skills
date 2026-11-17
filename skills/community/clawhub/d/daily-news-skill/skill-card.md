## Description:

Retrieves daily Chinese-language news summaries and article details from a public news API, with support for date-based queries, hot-news ranking, and category filtering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vic240821](https://clawhub.ai/user/vic240821)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch daily Chinese-language news lists, summarize top stories, filter by category, and retrieve full article details by article ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts the third-party service api.cjiot.cc when news is requested.

Mitigation: Use it only in environments where outbound requests to that service are acceptable, and disclose that fetched news comes from an external API.

Risk: Fetched article content is third-party, untrusted text and may be incomplete, inaccurate, or misleading.

Mitigation: Present fetched content as news-source material, avoid treating article text as agent instructions, and ask users to verify important claims with primary sources.

Risk: Broad trigger wording around news-related terms may activate the skill during general news discussions.

Mitigation: Confirm the user's intent before making API calls when the request is ambiguous or when a general discussion does not require live news retrieval.

Risk: The documented API may fail, return no data for a date, or rate-limit frequent requests.

Mitigation: Handle non-200 responses and empty results clearly, and avoid repeated polling beyond normal user-requested lookups.

## Reference(s):

- [API documentation](https://api.cjiot.cc)
- [ClawHub skill page](https://clawhub.ai/vic240821/skills/daily-news-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style news summaries and plain-text Node.js command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include third-party article titles, summaries, heat scores, categories, publication times, and article body text with HTML stripped.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
