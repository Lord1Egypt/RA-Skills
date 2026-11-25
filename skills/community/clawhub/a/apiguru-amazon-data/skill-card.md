## Description:

Fetches live Amazon marketplace data through Apiguru, including product details, prices, reviews, keyword search, best sellers, deals, stock, and seller profiles across 23 marketplaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apiguru-app](https://clawhub.ai/user/apiguru-app)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill for Amazon-only requests that need current product, review, price, offer, stock, seller, or keyword-search data, including monitoring by ASIN or Amazon URL.

### Deployment Geography for Use:

Global (23 supported Amazon marketplaces)

## Known Risks and Mitigations:

Risk: Calls beyond the free quota can incur charges when using an API key, and broad or batch requests may cost more.

Mitigation: Check the current quota and call price, then get user consent and agree on a spending cap before billable or batch requests.

Risk: The available security review is incomplete because some local references could not be resolved.

Mitigation: Review the unresolved local references before relying on the review, and limit credentials to the API-key file the user explicitly provides.

Risk: Feedback submitted through the skill appears on a public feedback wall.

Mitigation: Send only feedback the user has agreed to share, and exclude API keys, personal data, and private prompts or results.

## Reference(s):

- [Apiguru API documentation](https://agent.apiguru.app/llms-full.txt)
- [Endpoint reference](references/endpoints.md)
- [Pricing and errors](references/errors-and-costs.md)
- [Project homepage (skill metadata)](https://github.com/apiguru-app/agent-kit)

## Skill Output:

**Output Type(s):** [JSON data, Guidance]

**Output Format:** [Structured JSON results with concise usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result fields and size vary by endpoint and requested limit, compact mode, or field selection.]

## Skill Version(s):

1.1.69 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
