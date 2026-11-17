## Description:

Tracks Amazon New Releases and ranking data through the Clawec API, with optional category filtering for new-product monitoring, category bestseller discovery, product selection, and trend research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace operators and ecommerce researchers use this skill to query ClawEC for Amazon New Releases by category and summarize product lists, rankings, and trend observations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends category queries and an API bearer token to the external ClawEC service.

Mitigation: Use the CLAWEC_API_KEY environment variable, avoid hardcoding credentials, and run the skill only when use of ClawEC is acceptable.

Risk: Returned Amazon product data may influence product selection or other business decisions.

Mitigation: Review ClawEC account and API terms and verify important product, ranking, pricing, and link data before acting on it.

Risk: The API response data shape is dynamic and may vary across categories or responses.

Mitigation: Parse responses defensively, check status values, and summarize only fields actually returned by the API.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-amazon-new-release)
- [ClawEC API base URL](https://www.clawec.com/api)
- [Response schema reference](references/response-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with optional shell commands and JSON API response handling guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the CLAWEC_API_KEY environment variable and accepts an optional Amazon category code.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
