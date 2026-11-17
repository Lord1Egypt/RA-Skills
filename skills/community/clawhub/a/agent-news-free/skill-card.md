## Description:

A free AI enriched global news stream for agents, provided by agentnewsapi.com. Powered by $ANA on Solana.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentnewsdev](https://clawhub.ai/user/agentnewsdev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to fetch free, delayed Agent News API signals for monitoring global news, market-moving events, sentiment, entities, and categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Query terms and limit values are sent to agentnewsapi.com when the skill fetches news.

Mitigation: Avoid submitting sensitive or confidential query terms and review network use before deployment.

Risk: The skill returns third-party news data that may be delayed, incomplete, or unsuitable for automated decisions without review.

Mitigation: Treat returned signals as informational input and apply downstream validation or human review for high-impact use cases.

## Reference(s):

- [Agent News API homepage](https://agentnewsapi.com)
- [ClawHub skill page](https://clawhub.ai/agentnewsdev/skills/agent-news-free)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Free tier returns delayed news signals, is limited to 1 request per minute, and accepts limit and optional query parameters.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
