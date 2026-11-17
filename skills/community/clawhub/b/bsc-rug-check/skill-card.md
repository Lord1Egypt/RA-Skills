## Description:

Guides agents through paid EVM token safety screening and interpretation of a 0–100 heuristic score with auditable flags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perria080925-bot](https://clawhub.ai/user/perria080925-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Traders and agents use this skill to screen EVM token addresses before purchases or recommendations and review the returned safety flags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each lookup shares the queried token address with an external service and may authorize a $0.01 USDC payment.

Mitigation: Confirm the address and payment terms before submitting or authorizing a request.

Risk: A heuristic safety score cannot guarantee a token is safe.

Mitigation: Review the underlying flags and other evidence; do not treat the score as financial advice or a definitive verdict.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/perria080925-bot/skills/bsc-rug-check)
- [Token safety service](https://x402.bankr.bot/0xf436ca41bd0a236338bef57adeb4976677513010)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance for interpreting an external JSON score and safety flags; each paid request costs $0.01 USDC on Base.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
