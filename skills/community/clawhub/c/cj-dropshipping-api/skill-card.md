## Description: <br>
Guides agents through CJ Dropshipping API v2.0 authentication and common product, order, logistics, Shopify listing, delivery profile, and webhook workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simoncai519](https://clawhub.ai/user/simoncai519) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and e-commerce operators use this skill to integrate CJ Dropshipping workflows, issue authenticated API calls, manage products and Shopify listings, create orders, track logistics, and configure webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Runnable POST, order, payment, delivery-profile, and webhook commands can modify CJ or Shopify account state. <br>
Mitigation: Confirm the CJ account, shop, product IDs, customer data, costs, and callback URL before execution; prefer test accounts for validation. <br>
Risk: The CJ access token can authorize sensitive account actions. <br>
Mitigation: Protect the token, avoid logging it, and rotate or revoke credentials when they are no longer needed. <br>


## Reference(s): <br>
- [CJ Dropshipping API Reference](references/api-reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/simoncai519/cj-dropshipping-api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline bash and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a CJ access token; some example commands can modify CJ or Shopify account state.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
