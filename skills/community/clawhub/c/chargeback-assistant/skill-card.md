## Description: <br>
Helps consumers prepare payment-dispute and chargeback materials by identifying dispute type, mapping likely network reason codes, producing evidence checklists, drafting dispute letters, and summarizing deadlines and next steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hgereat](https://clawhub.ai/user/hgereat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to structure consumer chargeback and payment-dispute requests for Visa, Mastercard, American Express, PayPal, and Stripe-related transactions. It produces a situation assessment, reason-code guidance, a tailored evidence checklist, a draft dispute letter, and deadline-oriented next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chargeback deadlines, reason codes, and provisional-credit expectations may be incorrect for a user's specific issuer, payment platform, jurisdiction, or transaction facts. <br>
Mitigation: Tell users to verify deadlines, reason-code fit, and procedural requirements with their bank, card issuer, or payment platform before submitting a dispute. <br>
Risk: Users may share sensitive payment details while preparing dispute materials. <br>
Mitigation: Advise users to avoid sharing full card numbers, account credentials, passwords, and other highly sensitive identifiers in chat. <br>
Risk: A drafted dispute letter could be misused for an illegitimate or already-refunded chargeback. <br>
Mitigation: Follow the skill's honest-limits guidance by refusing friendly-fraud framing and by redirecting invalid, already-refunded, or buyer's-remorse cases to appropriate alternatives. <br>


## Reference(s): <br>
- [Visa Dispute Reference](references/visa.md) <br>
- [Mastercard Dispute Reference](references/mastercard.md) <br>
- [American Express Dispute Reference](references/amex.md) <br>
- [PayPal & Stripe Dispute Reference](references/paypal-stripe.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/hgereat/chargeback-assistant) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/hgereat) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces consumer-facing dispute assessments, evidence checklists, draft letters, and next-step guidance; users should verify deadlines and financial advice with their issuer or payment platform.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
