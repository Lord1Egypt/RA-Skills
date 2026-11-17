## Description:

Sell print-on-demand merchandise on Clawver. Browse Printful catalog, create product variants, track fulfillment and shipping. Use when selling physical products like posters, t-shirts, mugs, or apparel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nwang783](https://clawhub.ai/user/nwang783)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, sellers, and agent operators use this skill to create and manage Clawver print-on-demand merchandise, including product planning, Printful catalog selection, variant setup, design uploads, mockup generation, publishing, and fulfillment tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables authenticated operations against a Clawver print-on-demand account.

Mitigation: Install and use it only when the agent is expected to operate that account, and provide CLAW_API_KEY only in trusted agent environments.

Risk: Product plans, generated designs, mockups, and live listings may affect a seller's storefront and customers.

Mitigation: Review proposed plans before approval and require explicit confirmation before publishing products live.

Risk: AI design and mockup generation can spend credits, especially during retries.

Mitigation: Use idempotency keys for generation requests and create new keys only when the request payload materially changes.

Risk: Webhook destinations and uploaded design data can expose operational or creative assets if misconfigured.

Mitigation: Use trusted webhook URLs with strong secrets and review uploaded design data before submitting it to the platform.

Risk: Incorrect Printful variant IDs, stock fields, or empty variant arrays can block publishing or checkout.

Mitigation: Use string Printful IDs, configure non-empty variants before activation, and keep stock metadata current.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nwang783/skills/clawver-print-on-demand)
- [Clawver store](https://clawver.store)
- [Print-on-Demand API Examples](references/api-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash, curl, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a CLAW_API_KEY environment variable for authenticated Clawver API operations.]

## Skill Version(s):

1.0.12 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
