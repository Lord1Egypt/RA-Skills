## Description:

Daily e-commerce intelligence for Indian Flipkart and Amazon India sellers that tracks orders, returns, inventory levels, competitor pricing, Buy Box status, and WhatsApp morning summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utsavs](https://clawhub.ai/user/utsavs)

### License/Terms of Use:


## Use Case:

External marketplace sellers use this skill to monitor Flipkart seller operations from WhatsApp, including orders, returns, inventory, competitor prices, Buy Box status, and scheduled business summaries. Sellers may optionally connect Amazon India data for cross-market visibility.

### Deployment Geography for Use:

India

## Known Risks and Mitigations:

Risk: The skill can make live marketplace account changes, including listing price updates and order cancellations.

Mitigation: Use restricted API credentials where possible and require explicit approval before production price changes or cancellations.

Risk: WhatsApp commands could expose operational controls to an unintended sender.

Mitigation: Confirm which users are authorized to send commands before connecting the skill to a real seller account.

Risk: The price-update flow lacks explicit guardrails in the reviewed security evidence.

Mitigation: Set account-level limits or an approval workflow for price changes before allowing automated updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/utsavs/skills/flipkart-seller-dashboard)
- [Publisher profile](https://clawhub.ai/user/utsavs)
- [Flipkart Marketplace Seller API](https://api.flipkart.net/sellers/)
- [Flipkart Seller OAuth token endpoint](https://api.flipkart.net/sellers/oauth-service/oauth/token)
- [Amazon India Selling Partner API endpoint](https://sellingpartnerapi-fe.amazon.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, shell commands, guidance]

**Output Format:** [Markdown-style WhatsApp summaries, alerts, command responses, JSON configuration, and cron command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Flipkart API credentials; Amazon India support is optional when SP-API credentials are configured.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
