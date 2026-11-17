## Description:

Pull a Facebook page's profile, posts, reels and photos, one post with its comments, a single reel/video with downloadable URLs, a public group and its posts, an event, and hashtag posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to retrieve structured public Facebook page, post, reel, group, event, hashtag, and comment data through Scavio's API for brand monitoring, competitor analysis, and content research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Scavio API key and performs calls to a third-party provider.

Mitigation: Install only when use of Scavio is acceptable, provide SCAVIO_API_KEY through a secret or environment variable, and keep the key out of source control.

Risk: Credit-based billing and rate limits can affect cost and reliability.

Mitigation: Monitor credits and handle 402 and 429 responses before running repeated or automated collection.

Risk: Facebook profiles, posts, and comments can involve real people and public contact details.

Mitigation: Summarize results, avoid profiling private individuals, and return only data supplied by the API.

Risk: Downloadable reel and video URLs have short expirations.

Mitigation: Use downloadable URLs promptly and avoid retaining expiring URLs longer than needed.

## Reference(s):

- [Scavio Documentation](https://scavio.dev/docs?utm_source=agent-skills&utm_medium=skill&utm_campaign=facebook-scraper-api)
- [Scavio Rate Limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=facebook-scraper-api)
- [ClawHub Skill Page](https://clawhub.ai/scavio-ai/skills/facebook-scraper-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API responses and inline Python or curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCAVIO_API_KEY; API responses use a JSON envelope with data, response_time, credits_used, and credits_remaining.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
