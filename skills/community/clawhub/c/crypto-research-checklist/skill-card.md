## Description:

Runs a crypto project fundamentals checklist covering token data, liquidity, contract safety, team signals, protocol health, and a PASS/WATCH/FLAG verdict.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trdyqs6bsr-lksnf](https://clawhub.ai/user/trdyqs6bsr-lksnf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to perform structured crypto due diligence before investment decisions, including liquidity, holder concentration, contract, team, and protocol checks. It is intended to summarize risk signals without giving buy, sell, hold, or price-target advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends crypto research queries and payment-related metadata to an external API.

Mitigation: Use it only when the user is comfortable sharing that data with the listed API, and avoid sending unnecessary wallet, identity, or transaction details.

Risk: The skill steers users through paid calls, credit bundles, referrals, and Telegram subscriptions with weak consent and privacy boundaries.

Mitigation: Require explicit user consent before paid requests, referrals, subscriptions, or sharing chat identifiers.

Risk: A wallet-capable agent could sign or send USDC without sufficient user confirmation.

Mitigation: Do not allow signing or payment unless the user explicitly approves the recipient, chain, token, amount, fees, and purpose for that transaction.

Risk: Crypto research output could be mistaken for financial advice.

Mitigation: Present findings as due-diligence guidance only, avoid buy, sell, hold, or price-target recommendations, and state uncertainty when data is stale or incomplete.

## Reference(s):

- [Crypto Research Checklist on ClawHub](https://clawhub.ai/trdyqs6bsr-lksnf/skills/crypto-research-checklist)
- [Crypto Research API](https://crypto-api-blush.vercel.app)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with a verdict, checklist, risks, and context]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference external API responses, payment status, and source availability when producing the report.]

## Skill Version(s):

1.2.0 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
