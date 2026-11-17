## Description:

Browser-driven adidas Click B2B toolkit that places purchase orders, checks live inventory and wholesale pricing, and retrieves shipment tracking from the adidas Click portal through Playwright because adidas exposes no public API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmtucker](https://clawhub.ai/user/zmtucker)

### License/Terms of Use:

MIT-0

## Use Case:

External teams and purchasing agents use this skill with authorized adidas Click accounts to draft or submit purchase orders, check live stock, restock dates, and wholesale pricing, and retrieve shipment tracking for purchase orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use live adidas Click credentials and submit real purchase orders.

Mitigation: Install it only for authorized accounts, require literal JSON true before submitting an order, and use confirm=false review runs before live submission when practical.

Risk: Credentials and screenshots can expose sensitive account or order data.

Mitigation: Avoid inline or CLI passwords when possible, keep screenshots in a private controlled directory or disable them, and run the skill under an isolated unprivileged account.

Risk: Browser automation depends on approved adidas hosts and may trigger anti-bot controls.

Mitigation: Restrict the base URL to approved adidas hosts, review automation use against adidas terms, and use an authorized network path for the account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zmtucker/skills/drivethru-adidas-click)
- [adidas Click B2B portal](https://b2bportal.adidas-group.com)
- [Order flow notes](references/order_flow_notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON results, Markdown tracking tables, and concise operational guidance with shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Purchase-order submission requires confirm=true; inventory and tracking checks are read-oriented, while pricing briefly creates and deletes a DO NOT BUY cart.]

## Skill Version(s):

0.9.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
