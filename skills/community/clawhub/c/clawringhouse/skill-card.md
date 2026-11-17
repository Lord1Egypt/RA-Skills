## Description:

Clawringhouse helps agents research shopping options, compare products, and present budget-conscious recommendations or prepared carts for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[francoisjosephlacroix](https://clawhub.ai/user/francoisjosephlacroix)

### License/Terms of Use:

MIT

## Use Case:

External users and their agents use this skill to find product recommendations for gifts, pet care, household supplies, and similar shopping needs while keeping final purchase approval with the human.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopping queries, personal context, and product preferences may be sent to the Clawringhouse API.

Mitigation: Share only the context needed for the shopping request and avoid sending sensitive personal, account, or payment details.

Risk: The skill encourages use of logged-in browser sessions and cart changes.

Mitigation: Require explicit user approval before using any logged-in browser session or modifying a cart, and show the exact account, items, prices, links, and affiliate behavior first.

Risk: Product and cart links may include affiliate tracking.

Mitigation: Disclose affiliate-link behavior clearly and let the user choose whether to open or use those links.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/francoisjosephlacroix/skills/clawringhouse)
- [Clawringhouse API](https://clawringhouse.onrender.com)
- [Clawringhouse Website](https://clawringhouse.shop)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with inline Python and shell examples plus product or cart links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include affiliate-tagged Amazon links and API response examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
