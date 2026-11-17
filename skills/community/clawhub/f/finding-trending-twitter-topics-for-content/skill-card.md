## Description:

Finds trending Twitter/X topics and conversations with apidojo's Apify tweet scraper, returning topic volume signals, high-engagement posts, and content angle suggestions for content teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External content marketers, social media managers, newsletter writers, and real-time content teams use this skill to research active Twitter/X conversations in a niche and turn them into timely content opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The REST fallback shows an Apify API token passed in a URL, which can expose credentials through logs, shell history, or monitoring tools.

Mitigation: Use an authorization header or managed Apify tooling, keep tokens in protected environment variables, and avoid placing secrets in URLs.

Risk: Search queries can reveal confidential campaign, customer, or strategy terms to an external scraping service.

Mitigation: Review queries before execution and avoid submitting confidential or sensitive business terms.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-trending-twitter-topics-for-content)
- [Publisher profile: apidojo-io](https://clawhub.ai/user/apidojo-io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown brief with tables, scored topic clusters, top tweet examples, and optional shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tweet volume signals, engagement scores, freshness scoring, hashtag maps, and content angle recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
