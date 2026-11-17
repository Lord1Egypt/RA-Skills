## Description:

Uses a logged-in Chrome browser relay to search Coupang, compare products, inspect and manage cart items, and summarize checkout review before final ordering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mnemosyn1154](https://clawhub.ai/user/mnemosyn1154)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to have an agent search Coupang in an already logged-in Chrome session, compare product options, manage cart contents, and prepare a checkout review without submitting an order.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill operates in a logged-in Coupang session and can change cart contents.

Mitigation: Use it for search, comparison, cart review, and clearly requested cart edits; review the cart before checkout and do not use it to submit orders.

Risk: Batch mode can automatically choose products and add multiple items to the cart without intermediate confirmation.

Mitigation: Avoid batch mode unless that behavior is intended, or explicitly constrain acceptable products, quantities, and selection criteria before running it.

Risk: Saved operating memory may contain shopping preferences or cart history.

Mitigation: Review memory notes regularly and do not store passwords, card numbers, authentication codes, full addresses, phone numbers, or customs identifiers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mnemosyn1154/skills/coupang-shopping-relay)
- [Browser Relay Workflow](references/browser-relay-workflow.md)
- [Coupang Page Structure](references/coupang-page-structure.md)
- [Operating Memory](references/operating-memory.md)
- [Coupang Browser Automation Improvement Log](references/improvement-log.md)
- [Coupang Relay Memory Template](assets/coupang-relay-memory-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summaries, numbered lists, and concise status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product names, prices, quantities, delivery labels, failure notes, and checkout review summaries.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
