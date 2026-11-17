## Description:

蛋糕叔叔商城点单助手 helps users order cakes, desserts, snacks, and flowers from dangaoss.com by managing delivery addresses, searching products, generating payment links, and checking order status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhang1058](https://clawhub.ai/user/zhang1058)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers use this skill to complete an agent-guided dangaoss.com ordering flow, including token-based account access, delivery address selection or creation, product search, payment-link generation, and order status lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store account tokens, delivery addresses, phone numbers, and order identifiers in local plaintext memory.

Mitigation: Use it only on a trusted machine, keep token files out of version control, restrict local file access, and rotate the token if it may have been exposed.

Risk: The skill uses broad local command execution to make account-linked shopping API calls.

Mitigation: Review commands before execution and use the skill only when you trust the publisher and the dangaoss.com service.

Risk: Generated order links can initiate a real purchase flow tied to the user's account and selected delivery address.

Mitigation: Confirm the product, specification, quantity, and delivery address before opening or paying through the generated order link.

## Reference(s):

- [API docs](artifact/references/api_docs.md)
- [ClawHub skill listing](https://clawhub.ai/zhang1058/skills/dangaoss-cake)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with tables, inline links, and JSON command arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce account-linked order URLs and update local plaintext token, address, and order memory.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
