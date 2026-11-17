## Description:

Pull Douyin videos, user profiles and feeds, comments, hashtags, music, live rooms, the hot-search board, keyword search across videos, users, music and hashtags, and live-room lookup by creator.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to retrieve structured Douyin social-media data for creator analysis, trend monitoring, search, and public content review through the Scavio API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Douyin links, profile identifiers, search terms, and retrieved public social-media data are sent to Scavio under the user's API key.

Mitigation: Use the skill only for acceptable public-data workflows, avoid sensitive research terms or non-public personal data, and summarize comments or profiles instead of building dossiers on individuals.

Risk: Search endpoints consume 10 credits per call and repeated searches can create unexpected API costs.

Mitigation: Monitor credits_used and credits_remaining, avoid tight search loops, and prefer lower-cost endpoints when a resolved identifier is available.

Risk: Trending boards, hot-search results, rankings, and live status are point-in-time snapshots.

Mitigation: Re-fetch time-sensitive data before acting on it and avoid presenting stale counts, comments, follower numbers, or live status as current.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scavio-ai/skills/douyin-scraper-api)
- [Scavio documentation](https://scavio.dev/docs?utm_source=agent-skills&utm_medium=skill&utm_campaign=douyin-scraper-api)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=douyin-scraper-api)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with API examples and JSON response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCAVIO_API_KEY; API responses use structured JSON envelopes with data, response_time, credits_used, and credits_remaining.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
