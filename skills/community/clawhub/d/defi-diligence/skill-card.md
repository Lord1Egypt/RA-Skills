## Description:

Verifies Base or Solana crypto tokens before purchase by returning PASS/WATCH/FLAG verdicts, critical risk checks, scored checkpoints, and a paid x402 path for the full report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trdyqs6bsr-lksnf](https://clawhub.ai/user/trdyqs6bsr-lksnf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to screen unverified Base or Solana token symbols or contract addresses before a potential purchase. It provides token risk verdicts and checkpoint data while avoiding price targets or financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A third-party crypto screening service receives submitted token symbols or contract addresses.

Mitigation: Use the skill only when sharing token queries with the publisher is acceptable, and avoid submitting sensitive trading intent when unnecessary.

Risk: The paid full report can trigger a $2 USDC x402 payment flow.

Mitigation: Require explicit user approval and wallet confirmation that shows the network, recipient, amount, fees, and total before every payment.

Risk: The artifact text says an x402 wallet layer can handle payment automatically.

Mitigation: Disable unattended auto-pay for this skill or enforce a wallet policy that blocks payment without a per-transaction user confirmation.

Risk: A token-risk verdict could be mistaken for investment advice.

Mitigation: Present outputs as risk screening data only and avoid price targets, purchase recommendations, or fabricated reports for unresolved symbols.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/trdyqs6bsr-lksnf/skills/defi-diligence)
- [Publisher profile](https://clawhub.ai/user/trdyqs6bsr-lksnf)
- [Service homepage](https://crypto-api-blush.vercel.app)
- [OpenAPI schema](https://crypto-api-blush.vercel.app/openapi.json)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or JSON-style token risk report with PASS/WATCH/FLAG verdicts and checkpoint details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include an x402 payment challenge for a $2 USDC full report; outputs should remain verdict and risk data, not financial advice.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
