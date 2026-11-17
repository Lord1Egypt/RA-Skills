## Description:

CreditClaw helps agents register owner-controlled wallets, check balances and spending rules, make guarded purchases, request top-ups, generate payment links, and review transaction history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jononovo](https://clawhub.ai/user/jononovo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent perform financial workflows through CreditClaw, including wallet registration, spending checks, owner-governed purchases, top-up requests, payment link creation, and transaction review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad money-moving authority through wallet purchases, top-up requests, payment links, and card checkout flows.

Mitigation: Install only when the user intends real financial workflows; use strict owner controls, low spending limits, and ask-before-everything approval.

Risk: Remote free-form notes are treated as instructions by the skill.

Mitigation: Keep owner notes narrow and operational; avoid broad commands or policy-changing instructions in the notes field.

Risk: A leaked CreditClaw API key can allow unauthorized financial actions.

Mitigation: Store CREDITCLAW_API_KEY in a secrets manager and send it only to CreditClaw API endpoints.

Risk: The documented curl install path retrieves mutable remote files.

Mitigation: Verify fetched files against trusted hashes or review the downloaded files before installation.

Risk: Payment workflows may expose payer emails or full resource URLs containing private information.

Mitigation: Minimize sensitive data in payer_email, callback_url, merchant_url, and resource_url fields before submission.

## Reference(s):

- [CreditClaw Homepage](https://creditclaw.com)
- [CreditClaw Skill API Reference](https://creditclaw.com/skill.md)
- [CreditClaw Heartbeat Routine](https://creditclaw.com/heartbeat.md)
- [CreditClaw Skill Metadata](https://creditclaw.com/skill.json)
- [ClawHub Skill Listing](https://clawhub.ai/jononovo/skills/citi)
- [ClawHub Publisher Profile](https://clawhub.ai/user/jononovo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline JSON examples and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated API workflows; registration returns credentials that must be stored securely.]

## Skill Version(s):

1.0.6 (source: ClawHub release evidence); bundled artifact reports CreditClaw 2.0.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
