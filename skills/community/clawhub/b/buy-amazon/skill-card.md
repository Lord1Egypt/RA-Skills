## Description:

Searches Amazon.com through buystuff.ai, compares product data, builds carts, checks out to a US shipping address, requests a user-paid payment link, and tracks orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucasgeeksinthewood](https://clawhub.ai/user/lucasgeeksinthewood)

### License/Terms of Use:


## Use Case:

External users and AI agents use this skill to search Amazon products, compare price and rating signals, assemble carts, collect US shipping and email details, request payment-link emails after explicit approval, and track resulting orders.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill uses buystuff.ai as a third-party shopping intermediary for search, cart, checkout, and payment-link email.

Mitigation: Install it only when that intermediary is acceptable, and use it only for explicit shopping or ordering tasks.

Risk: Session IDs can connect cart state, checkout details, and order actions.

Mitigation: Keep each session ID scoped to one user and one transaction.

Risk: Requesting the payment link sends an actionable checkout email to the user.

Mitigation: Review the full price breakdown and shipping address with the user, then request the payment link only after clear approval.

Risk: Checkout requires shipping address and email information for fulfillment and payment-link delivery.

Mitigation: Collect only the required fulfillment details and avoid using the skill for unrelated personal-data handling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lucasgeeksinthewood/skills/buy-amazon)
- [buystuff.ai](https://buystuff.ai)
- [Rainforest API](https://www.rainforestapi.com/)

## Skill Output:

**Output Type(s):** [text, API calls, shell commands, guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Session-aware shopping flow using X-Session-ID; outputs include product comparisons, checkout summaries, payment-link requests, and order status.]

## Skill Version(s):

1.2.4 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
