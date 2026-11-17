## Description:

Search G2 software products, inspect profiles and pricing, and retrieve faceted reviews and per-star ratings through Scavio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and software buyers use this skill to compare B2B products, inspect pricing and features, and analyze customer reviews by rating or buyer segment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, product identifiers, review filters, and an API key are sent to Scavio.

Mitigation: Avoid sensitive queries and keep SCAVIO_API_KEY in a protected environment variable.

Risk: Repeated requests and pagination consume 5 credits per G2 call, including some failed requests.

Mitigation: Confirm the planned credit spend before multi-page pulls, limit retries, and avoid bulk profile requests.

Risk: An empty filtered review result can be mistaken for a lack of customer feedback.

Mitigation: Recheck without filters before drawing conclusions about review sentiment.

## Reference(s):

- [Scavio G2 search documentation](https://scavio.dev/docs/g2-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=g2-software-reviews-api)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=g2-software-reviews-api)
- [ClawHub skill listing](https://clawhub.ai/scavio-ai/skills/g2-software-reviews-api)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands]

**Output Format:** [Markdown summaries with structured review data and optional API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCAVIO_API_KEY; each G2 request costs 5 credits.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
