## Description:

Helps consumers classify payment disputes, map them to network or platform reason codes, gather evidence, and draft chargeback dispute letters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgereat](https://clawhub.ai/user/hgereat)

### License/Terms of Use:

MIT-0

## Use Case:

External consumers use this skill to prepare chargeback or payment dispute submissions by identifying the dispute type, matching the relevant Visa, Mastercard, American Express, PayPal, or Stripe path, assembling evidence, and drafting a submission letter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial dispute guidance may be outdated or misapplied to a user's issuer, payment network, or facts.

Mitigation: Verify deadlines, reason codes, and evidence requirements with the card issuer or payment platform before acting.

Risk: A user could submit unsupported or illegitimate dispute claims.

Mitigation: Submit only factual, supported disputes and use the skill's honest-limits checks for weak or invalid cases.

Risk: The artifact README's installer example uses @latest.

Mitigation: Prefer a pinned or otherwise verified ClawHub installer when installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hgereat/skills/chargeback-assistant)
- [Visa Dispute Reference](artifact/references/visa.md)
- [Mastercard Dispute Reference](artifact/references/mastercard.md)
- [American Express Dispute Reference](artifact/references/amex.md)
- [PayPal & Stripe Dispute Reference](artifact/references/paypal-stripe.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown response with situation assessment, reason code, tailored evidence checklist, dispute letter, deadline, and next steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bracketed placeholders for user-specific details; no automatic filing or external actions.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
