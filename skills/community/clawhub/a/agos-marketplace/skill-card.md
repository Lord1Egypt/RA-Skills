## Description:

Integrate OpenClaw with Agos Marketplace and automatically execute both sell-side listing creation and buy-side order creation through executable scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielw8088](https://clawhub.ai/user/danielw8088)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to automate AGOS marketplace seller listings and buyer purchase orders, including payment-parameter preparation and purchase-status tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create live AGOS marketplace listings and purchase orders through external API calls.

Mitigation: Require human review before running live scripts, verify wallet addresses and listing or task data, and use the listing script's dry-run mode before creating seller listings.

Risk: The order creation script has no dry-run mode and may send buyer wallet and task data to market.agos.fun.

Mitigation: Run create_order.py only after confirming the selected listing, buyer wallet, input payload, and whether payment preparation or status polling is intended.

Risk: Chain payment still requires a signer path outside the skill.

Mitigation: If a signer is unavailable or not approved, return payment_preparation fields for manual or external execution instead of attempting payment.

## Reference(s):

- [Agos Marketplace skill page](https://clawhub.ai/danielw8088/skills/agos-marketplace)
- [Publisher profile](https://clawhub.ai/user/danielw8088)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Seller flow returns service_id and service; buyer flow returns purchase, selected_listing_id, optional payment_preparation, and optional final_state.]

## Skill Version(s):

1.2.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
