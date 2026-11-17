## Description:

Look up products in the Stripe catalog and create a Stripe Checkout Session that returns a hosted checkout URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmtucker](https://clawhub.ai/user/zmtucker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Stripe product catalog entries and create hosted Checkout Session links for one-time payments, subscriptions, or setup flows. It is suited for workflows where the agent can safely use a Stripe secret key from the host environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A live Stripe key can create checkout links for real-money transactions.

Mitigation: Prefer test-mode or restricted keys and review the checkout mode and amount before creating live sessions.

Risk: Returned Checkout Session URLs can be used by anyone who has the link.

Mitigation: Share checkout URLs only with the intended customer and avoid logging them in broad-access channels.

Risk: Unpinned Stripe SDK installs can change behavior over time.

Mitigation: Pin or lock the Stripe SDK version when reproducible deployment behavior is required.

## Reference(s):

- [Stripe Checkout Sessions API](https://stripe.com/docs/api/checkout/sessions)
- [Create a Checkout Session](https://stripe.com/docs/api/checkout/sessions/create)
- [Stripe Search](https://stripe.com/docs/search)
- [Stripe API Keys](https://dashboard.stripe.com/apikeys)
- [Checkout Session Options](references/checkout_options.md)
- [ClawHub Skill Page](https://clawhub.ai/zmtucker/skills/drivethru-stripe)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON from helper scripts, with Markdown guidance from the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates Stripe API calls when invoked with STRIPE_SECRET_KEY; returns product details or a hosted Checkout Session URL.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
