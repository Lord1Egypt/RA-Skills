## Description:

Crisp Grocery helps agents plan groceries with Crisp, inspect user-authorized account data, compare promotions, check delivery windows and fees, fetch recipe or product images, and prepare confirmed basket changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeflow](https://clawhub.ai/user/zeflow)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Crisp Grocery to plan meals and grocery baskets from their own authorized Crisp account data, including promotions, order history, delivery windows, fees, and recipe or product details. The skill is read-only by default and supports basket edits only after exact user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper handles Crisp account bearer tokens and private account data.

Mitigation: Use a dedicated Crisp token when possible, keep token files in private locations with restrictive permissions, and do not include tokens in generated files or submissions.

Risk: Custom endpoints or CRISP_API_BASE could send authenticated requests somewhere unexpected.

Mitigation: Avoid custom endpoints and custom CRISP_API_BASE values unless the helper configuration has been reviewed for the intended session.

Risk: Saved raw account responses can expose private grocery, address, payment, delivery, invoice, or order-history data.

Mitigation: Save only sanitized summaries by default and avoid shared or version-controlled output folders for account responses.

Risk: Basket edits can change the user's Crisp cart contents.

Mitigation: Require an exact user confirmation naming the product or recipe, quantity, and intended action, then re-fetch the basket before reporting the result.

## Reference(s):

- [Crisp API Map](references/api-map.md)
- [Planning Rules](references/planning-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands, JSON summaries, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Crisp API reads and confirmed basket changes; should avoid exposing tokens or private account fields by default.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
