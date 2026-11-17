## Description:

Browser shopping assistant that compares browser-visible prices, seller type, reviews, promotions, delivery and return signals, and after-sales risk across shopping sites, then recommends whether to buy, wait, switch platform, or avoid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers use this skill to compare visible ecommerce listings, promotions, seller and review signals, delivery and return terms, and purchase risks before making their own buying decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shopping workflow may encounter credential, identity, address, or payment fields.

Mitigation: Do not enter or provide credentials, SMS codes, passwords, CAPTCHA responses, identity details, addresses, or payment data.

Risk: The agent could be asked to complete a purchase action.

Mitigation: Do not submit orders, click checkout, click final confirmation, or initiate payment; the user must complete any purchase manually.

Risk: Visible price, stock, coupon, delivery, return, and after-sales terms may change or vary by account, location, or time.

Mitigation: Require the user to recheck final purchase terms directly on the shopping site before buying.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/browser-e-commerce)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown shopping comparison with buy, wait, switch-platform, or avoid recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses browser-visible or user-provided information only; no login, checkout, order submission, or payment; users must recheck final price, stock, delivery, coupons, and after-sales terms before purchase.]

## Skill Version(s):

0.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
