## Description:

Search and order pharmacy products from apohealth.de via apo-cli, including medication search by name or PZN, product details, category browsing, and cart management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lars147](https://clawhub.ai/user/lars147)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill for deliberate apohealth.de shopping tasks: searching pharmacy products, reviewing prices and availability, browsing categories, and building a cart for the user to inspect and check out themselves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change a health-related shopping cart.

Mitigation: Use it only for deliberate apohealth.de shopping tasks, show prices to the user, and require user confirmation before cart clearing or other destructive cart changes.

Risk: The skill may be mistaken for medical advice because it searches medication and pharmacy products.

Mitigation: Keep responses limited to shopping, product lookup, pricing, availability, and cart management; do not use the skill for diagnosis, treatment recommendations, or general medical advice.

Risk: Cart cookies and tokens may be written locally in plaintext.

Mitigation: Use reviewed installations in appropriate environments and remove local apo_cookies.json and apo_cart.json files when the cart session should no longer persist.

Risk: The README installation command references a mutable Git source.

Mitigation: Prefer installing a pinned, reviewed revision for production or repeatable deployments.

Risk: Checkout should remain user-controlled.

Mitigation: Build the cart only, provide the apohealth.de cart URL for review, and leave final checkout and purchase completion to the user.

## Reference(s):

- [Apo Cli Skill Page](https://clawhub.ai/lars147/skills/apo-cli)
- [apohealth.de](https://www.apohealth.de)
- [Full Command Reference](references/commands.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with command examples, product/cart summaries, and apohealth.de cart URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The agent should show prices, request confirmation before destructive cart actions, and hand checkout to the user with a cart URL.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
