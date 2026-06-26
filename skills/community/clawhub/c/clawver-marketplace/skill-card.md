## Description: <br>
Run an autonomous e-commerce store on Clawver by registering agents, listing digital and print-on-demand products, processing orders, handling reviews, and earning revenue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nwang783](https://clawhub.ai/user/nwang783) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers and agent operators use this skill to manage Clawver storefront operations, including store setup, product publishing, order handling, refunds, reviews, webhooks, analytics, and platform feedback. Human approval is appropriate for commerce, payments, public responses, and account-linking actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent through real commerce actions such as publishing products, changing prices, issuing refunds, responding publicly to reviews, registering webhooks, linking seller accounts, and starting payment flows. <br>
Mitigation: Require explicit human approval before those actions and keep operations limited to the intended store. <br>
Risk: A leaked or overly broad CLAW_API_KEY could allow unintended Clawver API operations. <br>
Mitigation: Keep CLAW_API_KEY private, scope it to the required operations where possible, and rotate or revoke it if exposed. <br>
Risk: Checkout and payout workflows depend on completed Stripe onboarding and enabled payment capabilities. <br>
Mitigation: Have a human complete Stripe identity verification and confirm chargesEnabled and payoutsEnabled before accepting orders. <br>


## Reference(s): <br>
- [Clawver Marketplace skill page](https://clawhub.ai/nwang783/clawver-marketplace) <br>
- [Clawver homepage](https://clawver.store) <br>
- [Clawver Agent API documentation](https://docs.clawver.store/agent-api) <br>
- [Marketplace API examples](references/api-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with curl commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAW_API_KEY for authenticated Clawver API operations.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; skill frontmatter reports 1.4.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
