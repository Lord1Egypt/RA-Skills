## Description:

Guides agents through CJ Dropshipping API v2.0 authentication, product search, order creation, shipment tracking, Shopify listing management, logistics, delivery profiles, and webhook setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simoncai519](https://clawhub.ai/user/simoncai519)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and e-commerce operators use this skill to integrate CJ Dropshipping workflows, including API authentication, product and logistics queries, Shopify listing setup, order creation, shipment tracking, and webhook configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CJ API requests require CJ-Access-Token credentials.

Mitigation: Keep CJ-Access-Token values private and avoid pasting or logging tokens in shared contexts.

Risk: Order creation, payment, delivery profile, Shopify listing, and webhook operations can change business data.

Mitigation: Review generated commands and request bodies before execution, especially for order, payment, listing, profile, and webhook changes.

Risk: Order and shipment workflows may involve customer shipping details.

Mitigation: Share only the customer and order data required for the intended CJ Dropshipping operation.

Risk: Webhook setup can send account or order events to external callback URLs.

Mitigation: Verify webhook callback URLs and ownership before configuring them in CJ Dropshipping.

## Reference(s):

- [CJ Dropshipping API Reference](references/api-reference.md)
- [ClawHub skill page](https://clawhub.ai/simoncai519/skills/cj-dropshipping-api)
- [Publisher profile](https://clawhub.ai/user/simoncai519)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with shell command examples and API request snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CJ API requests that require a CJ-Access-Token and can modify e-commerce account data when executed.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
