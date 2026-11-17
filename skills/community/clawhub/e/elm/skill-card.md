## Description:

Assisted Ele.me ordering skill that turns a natural-language request plus delivery address, item name, requirements, and budget into a ready-to-pay cart: resume from a user-authenticated Ele.me session, search nearby merchants by address, compare real payable totals with visible coupons and discounts, and add the best basket to cart before handing off for payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn natural-language Ele.me food delivery requests into a prepared cart. It helps compare nearby merchants, coupons, red packets, fees, ETA, and basket fit after the user authenticates directly in the official Ele.me surface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect account-visible address, coupon, red-packet, and cart information in an already authenticated Ele.me session.

Mitigation: Use it only with explicit consent, let the user authenticate in the official Ele.me surface, and avoid storing or reusing account or session data.

Risk: The skill can modify the cart before payment, which may create an unwanted basket if constraints, substitutions, fees, or discounts are misread.

Mitigation: Stop before payment and have the user review the cart, address, coupon selection, delivery notes, and total before paying.

Risk: Handling login codes or passwords in chat would expose authentication secrets.

Mitigation: Do not ask for, copy, store, or type login secrets; pause while the user completes authentication themselves.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/elm)
- [README](README.md)
- [CHANGELOG](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown sections describing cart status, selected merchant and basket, savings, and payment handoff]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stops before payment and asks the user to review address, delivery notes, coupon selection, and total.]

## Skill Version(s):

2.0.1 (source: SKILL.md frontmatter, package.json, CHANGELOG, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
