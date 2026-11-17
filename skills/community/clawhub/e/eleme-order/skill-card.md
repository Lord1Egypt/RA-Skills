## Description:

Order food delivery from Ele.me (饿了么) using Playwright MCP browser automation while leaving payment to the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xbralready](https://clawhub.ai/user/xbralready)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to order food, drinks, or groceries from Ele.me through a browser workflow that searches restaurants, adds items to a cart, reviews checkout details, and stops for manual payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The browser workflow exposes Ele.me login, SMS verification, delivery address, cart, and checkout details to the agent session.

Mitigation: Use a trusted browser context, provide sensitive values only when needed, and review address, items, and total before order submission.

Risk: An order could be submitted with the wrong items, address, or total if checkout details are not reviewed carefully.

Mitigation: Pause at the confirmation page, present the order details to the user, and submit only after explicit user confirmation.

Risk: Using @playwright/mcp@latest can introduce dependency behavior changes over time.

Mitigation: Pin a tested Playwright MCP package version for stable operational use.

Risk: Payment credentials or biometric approvals are outside the safe automation boundary.

Mitigation: Keep payment manual and do not enter payment passwords or complete payment approval on the user's behalf.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xbralready/skills/eleme-order)
- [Publisher profile: xbralready](https://clawhub.ai/user/xbralready)
- [Ele.me H5 service](https://h5.ele.me)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON configuration and browser-action instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npx and a Playwright MCP server; order payment remains manual.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
