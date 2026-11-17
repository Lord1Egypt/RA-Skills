## Description:

Let your agent shop online with guardrailed wallets, multiple payment methods, and owner approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[triplehippo](https://clawhub.ai/user/triplehippo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent register a CreditClaw wallet, check spending rules, and make guarded online purchases through prepaid wallet, self-hosted card, or x402 payment flows with owner approval.

### Deployment Geography for Use:

Global, with Amazon purchase flows documented as limited to US shipping addresses.

## Known Risks and Mitigations:

Risk: The skill gives agents authority to make real purchases and move money through wallet, card, and payment-link flows.

Mitigation: Install only when that behavior is intended, keep CREDITCLAW_API_KEY in a secure secret store, use the strictest approval mode, and set low per-transaction, daily, and monthly limits.

Risk: Payment-link creation can charge third parties and was flagged by security evidence as under-disclosed.

Mitigation: Disable or tightly restrict payment-link creation unless receivables are needed, and require clear consent before using payer emails or sending payment links.

Risk: Purchasing flows may involve sensitive shipping addresses and payer contact details.

Mitigation: Share shipping addresses and payer emails only with explicit user consent and keep purchase confirmations visible to the owner.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/triplehippo/skills/apple)
- [CreditClaw Skill Guide](https://creditclaw.com/creditcard/skill.md)
- [Shopping Guide](https://creditclaw.com/creditcard/shopping.md)
- [Amazon Purchase Guide](https://creditclaw.com/creditcard/amazon.md)
- [Pre-paid Wallet Guide](https://creditclaw.com/creditcard/prepaid-wallet.md)
- [Self-Hosted Card Guide](https://creditclaw.com/creditcard/self-hosted-card.md)
- [Stripe x402 Wallet Guide](https://creditclaw.com/creditcard/stripe-x402-wallet.md)
- [Heartbeat Guide](https://creditclaw.com/creditcard/heartbeat.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown with inline JSON and bash/curl code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and owner-configured wallet or payment rails; purchases may require owner approval.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.3.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
