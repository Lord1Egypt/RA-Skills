## Description:

Live context layer for AI agents. One /ask endpoint for news, weather, crypto prices, and alerts. 228K+ articles, 3,576 feeds, 14 categories. Enriched with sentiment, entities, and credibility. Free to use, no API key needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[angpenghian](https://clawhub.ai/user/angpenghian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Agenttimes to retrieve current news, weather, crypto prices, trending stories, and topic alerts through the Agent Times API. It is useful when an agent needs live context from a single API surface and can process JSON responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user queries to the external agenttimes.live service.

Mitigation: Use it only when sharing the query with Agent Times is acceptable, and avoid sending sensitive or confidential data.

Risk: The /subscribe endpoint posts matching articles to a caller-provided public webhook and returns an unsubscribe secret.

Mitigation: Use only an intentional public HTTPS webhook URL and store the unsubscribe secret so subscriptions can be removed.

Risk: The /search endpoint is documented as a paid x402 request.

Mitigation: Confirm payment intent before using /search; prefer the documented free endpoints when paid web search is not needed.

## Reference(s):

- [Agent Times homepage](https://agenttimes.live)
- [Agent Times API documentation](https://agenttimes.live/info)
- [ClawHub skill listing](https://clawhub.ai/angpenghian/skills/agenttimes)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with curl examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for command examples; no API key is documented as required for the free endpoints.]

## Skill Version(s):

8.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
