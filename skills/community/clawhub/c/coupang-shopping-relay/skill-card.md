## Description: <br>
Uses a logged-in Chrome browser relay to search Coupang, compare products, manage cart items, and summarize the cart before checkout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mnemosyn1154](https://clawhub.ai/user/mnemosyn1154) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to shop on Coupang through an existing logged-in Chrome session, including product search, cart review, cart additions, deletions, quantity changes, and pre-checkout review. It is best suited for supervised cart management, not autonomous checkout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify a logged-in Coupang cart by adding, deleting, or changing quantities. <br>
Mitigation: Use supervised operation: preview products, options, quantities, and prices before cart changes, then review the cart before checkout. <br>
Risk: Batch mode may automatically select and add products without asking between each item. <br>
Mitigation: Reserve batch mode for clear multi-item requests, avoid it for ambiguous products, and require final cart review with success and failure details. <br>
Risk: Dynamic Coupang pages can make cart state hard to verify after writes. <br>
Mitigation: Wait for key page elements, re-read or screenshot the cart after changes, and treat unverified clicks as uncertain rather than successful. <br>
Risk: Shopping memory may retain cart history, screenshots, addresses, payment details, or sensitive preferences. <br>
Mitigation: Persist only non-sensitive operating notes unless the user explicitly wants shopping details saved; never store passwords, card numbers, authentication codes, full addresses, or customs IDs. <br>
Risk: Checkout-related screens can expose delivery and payment labels. <br>
Mitigation: Use checkout screens for read-only review, do not submit orders or change payment or delivery settings, and ask the user to handle authentication or sensitive entry directly. <br>


## Reference(s): <br>
- [Coupang Shopping Relay on ClawHub](https://clawhub.ai/mnemosyn1154/coupang-shopping-relay) <br>
- [Browser Relay Workflow](references/browser-relay-workflow.md) <br>
- [Coupang Page Structure](references/coupang-page-structure.md) <br>
- [Operating Memory](references/operating-memory.md) <br>
- [Coupang Browser Automation Improvement Log](references/improvement-log.md) <br>
- [Coupang Relay Memory Template](assets/coupang-relay-memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text summaries and structured guidance for browser relay actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include numbered product lists, success/failure cart-change summaries, price totals, and pre-checkout review notes.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
