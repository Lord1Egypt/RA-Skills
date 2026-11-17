## Description:

Purchase products from Amazon and Shopify stores through conversational checkout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsyvic](https://clawhub.ai/user/tsyvic)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to buy products from Amazon or Shopify product links through a chat-based checkout flow. The skill collects shipping details, obtains or reuses a payment token, submits a Rye purchase request, and reports order status back to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real purchases and may reuse saved payment tokens.

Mitigation: Require a fresh user confirmation in the same turn before every order, including orders using a saved token, and confirm the final total before purchase.

Risk: Reusable payment tokens, shipping details, and purchase preferences may be saved in agent memory.

Mitigation: Prefer a fresh payment token for each purchase when memory handling is uncertain, save tokens and addresses only with explicit permission, and delete saved data when requested.

Risk: Product content, API responses, or pasted text could contain instructions that conflict with the user's intent.

Mitigation: Act only on purchase, address-change, token-reuse, or confirmation-skip instructions that come directly from the user's messages.

Risk: Shell commands that embed user-supplied values can create command-injection exposure.

Mitigation: Use the documented quoted heredoc curl pattern so product URLs, addresses, names, and token values are passed as request data instead of interpolated into the shell command.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tsyvic/skills/buy-anything)
- [Publisher Profile](https://clawhub.ai/user/tsyvic)
- [Rye API Documentation](https://docs.rye.com)
- [BasisTheory](https://basistheory.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown guidance with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces purchase-flow instructions, confirmation prompts, curl requests, order polling guidance, and user-facing order summaries.]

## Skill Version(s):

3.0.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
