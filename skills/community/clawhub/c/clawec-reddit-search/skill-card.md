## Description:

Searches Reddit posts and discussions by keyword through the ClawEC API to support community sentiment, user-need, and product-idea research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to search public Reddit discussions through ClawEC, then summarize posts, engagement signals, and product or user-research observations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords are sent to ClawEC as a third-party API provider and authenticated with CLAWEC_API_KEY.

Mitigation: Avoid sensitive private search terms unless the use case permits it, read the key from the environment, and do not hard-code credentials.

Risk: Public Reddit discussions may be incomplete, noisy, or misleading as indicators of market demand.

Mitigation: Treat results as community discussion context, verify important claims, and do not present Reddit activity as sales data.

## Reference(s):

- [Reddit Search Response Schema](artifact/references/response-schema.md)
- [ClawEC API Base URL](https://www.clawec.com/api)
- [ClawEC API Key Page](https://www.clawec.com/api-key?source=q-clawhub)
- [ClawHub Skill Page](https://clawhub.ai/anyunzhong/skills/clawec-reddit-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries with tables and optional bash commands; API responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAWEC_API_KEY and sends the search keyword to the ClawEC API.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
