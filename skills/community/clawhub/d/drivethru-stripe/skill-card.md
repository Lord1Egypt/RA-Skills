## Description: <br>
Look up products in the Stripe catalog and create a Stripe Checkout Session that returns a hosted checkout URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zmtucker](https://clawhub.ai/user/zmtucker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and commerce teams use this skill to inspect Stripe products and create hosted Checkout Sessions for one-time payments, subscriptions, or setup flows after confirming the intended customer, items, and amount. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A live Stripe secret key can create real payment or subscription checkout sessions. <br>
Mitigation: Use Stripe test mode first, prefer restricted keys where possible, and require explicit confirmation of live mode, customer, items, and total amount before creating a session. <br>
Risk: The skill requires sensitive Stripe credentials. <br>
Mitigation: Provide STRIPE_SECRET_KEY through the agent host environment and do not paste or log the secret key in chat. <br>
Risk: Checkout URLs can be opened by anyone who receives the link. <br>
Mitigation: Share generated checkout URLs only with the intended customer or recipient. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zmtucker/drivethru-stripe) <br>
- [Checkout Session Options](references/checkout_options.md) <br>
- [Stripe Checkout Sessions API](https://stripe.com/docs/api/checkout/sessions) <br>
- [Create a Checkout Session](https://stripe.com/docs/api/checkout/sessions/create) <br>
- [Stripe Search](https://stripe.com/docs/search) <br>
- [Stripe API Keys](https://dashboard.stripe.com/apikeys) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON from helper scripts, plus concise text guidance for product lookup results, checkout URLs, and recoverable errors.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the stripe Python package, and STRIPE_SECRET_KEY supplied through the environment.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
