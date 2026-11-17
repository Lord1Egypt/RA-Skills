## Description:

Generates real-time, logical product bundles and cross-sell offers from cart contents to increase average order value and reduce checkout abandonment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rijoyai](https://clawhub.ai/user/rijoyai)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce merchants and store operators use this skill to convert current cart contents into product bundle proposals, cross-sell logic, discount rationales, and one-click checkout upsell copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may route general ecommerce marketing requests to this skill when strict skill routing is required.

Mitigation: Review the trigger wording during installation and route the skill primarily to cart, bundle, cross-sell, AOV, and checkout upsell requests.

Risk: Bundle recommendations can be commercially unsuitable if cart contents, product compatibility, inventory, shipping thresholds, or margin guardrails are incomplete.

Mitigation: Have the merchant verify proposed pairings, discount rationale, margin impact, inventory, fulfillment constraints, and policy claims before publishing the upsell.

## Reference(s):

- [Bundle and cross-sell playbook](artifact/references/bundle_playbook.md)
- [ClawHub skill release](https://clawhub.ai/rijoyai/skills/cart-bundle-aov-upsell)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown tables with concise implementation notes and checkout copy]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full bundle responses include main product, complement, bundle discount rationale, and one-click add copy.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
