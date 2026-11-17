## Description:

Pull Douyin videos, user profiles and feeds, comments, hashtags, music, live rooms, the hot-search board, and keyword search across videos, users, music, live and hashtags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, analysts, and agents use this skill to retrieve structured Douyin public-content data through Scavio API endpoints for creator analysis, trend spotting, social research, and search workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin URLs, identifiers, keywords, and related query parameters to Scavio's API under the user's API key.

Mitigation: Use only for legitimate research, minimize collection of personal or social-graph data, and confirm users are comfortable with third-party API processing before running requests.

Risk: The skill can retrieve public social-media data including comments, profiles, followers, following, likes, and creator activity.

Mitigation: Avoid profiling individuals, summarize people-generated content carefully, and respect platform rules and applicable privacy law.

Risk: Search endpoints consume more credits than other endpoints and loops can spend credits quickly.

Mitigation: Check credits_used on responses, avoid tight search loops, and throttle or stop pagination when cursors stop advancing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/scavio-ai/skills/douyin-api)
- [Scavio API Documentation](https://scavio.dev/docs?utm_source=agent-skills&utm_medium=skill&utm_campaign=douyin-scraper-api)
- [Scavio Rate Limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=douyin-scraper-api)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline JSON, Python, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCAVIO_API_KEY; API responses are structured JSON envelopes with data, response_time, credits_used, and credits_remaining.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
