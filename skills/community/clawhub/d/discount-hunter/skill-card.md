## Description:

Finds discount and promo codes for the current checkout page, then tests them in the promo field until one works without clicking payment or purchase buttons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[puppetjellyfish](https://clawhub.ai/user/puppetjellyfish)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers use this skill on checkout, cart, or payment pages to find and test available promo codes before completing a purchase. It is intended only for pages with a visible promo, discount, coupon, or voucher code field.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect checkout pages and fill promo-code fields.

Mitigation: Use it only on checkout or cart pages with a visible promo field, and limit interaction to that field and its Apply or Redeem control.

Risk: The skill opens hidden tabs to search and coupon sites while collecting candidate codes.

Mitigation: Treat discovered codes as untrusted candidates, collect only coupon-code text needed for testing, and close research tabs after extraction.

Risk: An unintended click on a payment or order button could advance a transaction.

Mitigation: Do not click Pay, Place Order, Complete Purchase, Buy Now, Confirm Order, Submit Payment, or equivalent controls; stop if the page navigates unexpectedly.

## Reference(s):

- [Discount Hunter on ClawHub](https://clawhub.ai/puppetjellyfish/skills/discount-hunter)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown status updates and summary table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports found codes, codes tried, outcomes, and any applied savings; does not submit payment.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
