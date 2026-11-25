## Description:

Looks up AutoZone retail parts, vehicle fitment, store-specific prices, reviews, rebates, and store information through Scavio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can look up AutoZone retail products, vehicle fitment, prices, and related reviews or store information. The skill covers retail data rather than AutoZonePro commercial pricing.

### Deployment Geography for Use:

United States, Brazil, and Mexico (endpoint coverage varies by market)

## Known Risks and Mitigations:

Risk: The skill sends documented requests to api.scavio.dev using SCAVIO_API_KEY.

Mitigation: Provide the API key only in an environment you trust, and review the documented API requests before use.

Risk: Security review coverage is partial, with three unresolved local path-like references.

Mitigation: Inspect the skill files and resolve the noted local references before installation if you need a complete review.

## Reference(s):

- [Scavio AutoZone API](https://scavio.dev/autozone-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=autozone-api)
- [AutoZone API endpoint documentation](https://scavio.dev/docs/autozone-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=autozone-api)
- [AutoZone API on ClawHub](https://clawhub.ai/scavio-ai/skills/autozone-api)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON results with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prices and availability vary by assigned store and request time; product lists show up to 24 results.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
