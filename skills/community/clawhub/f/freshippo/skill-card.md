## Description:

Freshippo helps users choose 盒马 products, compare freshness, price, and delivery timing, and prepare a manual shopping list without agent-controlled login, in-app product-list changes, coupon use, address choice, checkout, order submission, or payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill as a read-only grocery shopping decision assistant for Freshippo. It produces product comparisons, freshness and price checks, delivery-window advice, meal-planning support, and a shopping-list handoff for the user to complete manually.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A logged-in Freshippo browser session could expose shopping account state or enable unintended account-changing actions.

Mitigation: Use the skill in read-only decision-assist mode by default, watch any logged-in session use, and keep address selection, coupons, cart changes, delivery-slot reservation, checkout, and payment manual.

Risk: Prices, stock, freshness indicators, discounts, and delivery slots can change before purchase.

Mitigation: Have the user manually verify final price, stock, freshness, coupons, address, delivery slot, and payment details in the Freshippo app before ordering.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/freshippo)
- [Publisher profile](https://clawhub.ai/user/harrylabsj)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown shopping-list guidance with comparison tables and manual checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only decision assistance; no checkout, payment, address selection, coupon application, delivery-slot reservation, or in-app product-list changes.]

## Skill Version(s):

2.1.2 (source: SKILL.md frontmatter, package.json, clawhub.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
