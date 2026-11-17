## Description:

Fetches current product, price, review, offer, stock, seller, and keyword data from 23 Amazon marketplaces through Apiguru, with user approval required before billable calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apiguru-app](https://clawhub.ai/user/apiguru-app)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents can retrieve current product, pricing, review, offer, inventory, seller, and keyword data from Amazon marketplaces when a request calls for Amazon-specific information. The skill is intended for Amazon lookups and monitoring, not other retailers or general shopping advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Billable API calls can charge the user's account, and a timed-out keyed or paid call may still have completed.

Mitigation: Ask before billable calls, agree a spending cap, and do not automatically repeat a keyed or paid call that timed out.

Risk: The security assessment is benign but has medium confidence and partial coverage, with some skill references unresolved.

Mitigation: Review the unresolved references and skill content; do not treat the scan result as proof that the skill is risk-free.

Risk: The feedback command posts the supplied text to Apiguru's public feedback wall.

Mitigation: Submit only text the user intends to make public.

## Reference(s):

- [Endpoint reference](references/endpoints.md)
- [Costs, billing, and retries](references/errors-and-costs.md)
- [Apiguru API documentation](https://agent.apiguru.app/llms-full.txt)
- [Apiguru API endpoint and pricing schemas](https://agent.apiguru.app/.well-known/x402)
- [Apiguru agent-kit project homepage](https://github.com/apiguru-app/agent-kit)

## Skill Output:

**Output Type(s):** [JSON, Text, API calls]

**Output Format:** [Structured Amazon marketplace data as JSON or concise text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live results vary by endpoint and marketplace.]

## Skill Version(s):

1.1.65 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
