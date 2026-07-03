## Description: <br>
Provides UU Paotui same-city delivery and on-site errand workflows, including price quotes, order creation, order lookup, cancellation, payment handling, registration, and courier tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uupt-mcp](https://clawhub.ai/user/uupt-mcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to price, place, manage, cancel, and track UU Paotui same-city courier and errand orders through Node.js or Python commands. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create real-world delivery or errand orders and the artifact instructions say to create orders without a second confirmation. <br>
Mitigation: Require explicit user confirmation of the full order summary, recipient phone number, address, price, and service type before creating or canceling an order. <br>
Risk: The skill handles developer app secrets, openId values, phone numbers, addresses, payment links, and courier tracking data. <br>
Mitigation: Prefer environment variables or a secret store over config.json, avoid sharing credentials in chat, and redact personal data from logs and transcripts where possible. <br>
Risk: Payment links and WeChat QR generation may expose payment URLs to third-party services. <br>
Mitigation: Verify payment destinations before sharing links or QR codes, and use QR generation only when needed for the selected channel. <br>
Risk: The security verdict is suspicious because the skill has weak disclosure around sensitive delivery and payment data. <br>
Mitigation: Install only from the server-resolved publisher profile and review the skill behavior before granting access to real customer orders. <br>


## Reference(s): <br>
- [UU Paotui Open Platform](https://open.uupt.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/uupt-mcp/skills/bang-wo-pao-tui) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown/text with inline shell commands, script status tokens, order details, payment links, and optional QR image file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local config.json, create payment_qrcode.png, and return delivery addresses, phone numbers, payment URLs, order status, and courier tracking details.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata; artifact frontmatter and package.json list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
