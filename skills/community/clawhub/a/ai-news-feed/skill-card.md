## Description:

The AI News Feed API skill helps agents query a RapidAPI-hosted feed of real-time AI/ML news from curated Twitter/X accounts with bilingual summaries, importance scores, and topic tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fredhjc](https://clawhub.ai/user/fredhjc)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to retrieve current AI/ML news, trending topics, filtered topic feeds, account-specific posts, and weekly digests from the AI News Feed API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requests to a third-party RapidAPI service using a user-provided RapidAPI key.

Mitigation: Store the key securely, avoid exposing it in shared chats or logs, and call the API only when the user explicitly wants AI news from this feed.

Risk: News items and enriched summaries may be incomplete, stale, or misleading because they come from curated Twitter/X accounts and automated enrichment.

Mitigation: Treat results as news leads, keep source tweet links and UTC timestamps with important items, and verify high-impact claims against primary sources before acting.

## Reference(s):

- [AI News Feed API response schemas](references/api-spec.md)
- [RapidAPI AI News Feed listing](https://rapidapi.com/jiachenfred/api/twitter-ai-news-feed)
- [AI News Feed API base URL](https://twitter-ai-news-feed.p.rapidapi.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with REST endpoint examples, curl commands, and JSON response schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a user-provided RapidAPI key; API responses are JSON and tweetedAt timestamps are UTC.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
