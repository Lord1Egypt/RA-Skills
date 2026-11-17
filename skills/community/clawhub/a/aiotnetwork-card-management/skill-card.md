## Description:

Create and manage virtual cards via MasterPay Global. Supports single-use cards for one-time purchases and multi-use cards for repeated use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[d9m1n1c](https://clawhub.ai/user/d9m1n1c)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create virtual payment cards, inspect card and wallet status, retrieve card details, and manage card lifecycle actions such as lock, unlock, and cancellation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive payment actions and card data, including bearer tokens, full card numbers, CVVs, and PINs.

Mitigation: Use only a trusted HTTPS API base URL, keep bearer tokens and PINs out of logs, and never persist full card numbers or CVVs.

Risk: Card ATM PINs may be exposed by card creation, list, and detail responses without requiring a transaction PIN.

Mitigation: Redact ATM PINs by default and require explicit user confirmation or step-up verification before revealing them.

Risk: Card cancellation is irreversible.

Mitigation: Require clear user confirmation and fresh transaction PIN verification before cancellation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/d9m1n1c/skills/aiotnetwork-card-management)
- [Publisher profile](https://clawhub.ai/user/d9m1n1c)
- [Default AIOT payment API base URL](https://payment-api-dev.aiotnetwork.io)

## Skill Output:

**Output Type(s):** [text, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with API endpoint references and environment configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authentication for payment operations; some sensitive actions require a fresh transaction PIN.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
