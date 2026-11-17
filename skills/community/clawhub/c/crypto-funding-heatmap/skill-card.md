## Description:

Shows cross-venue perpetual futures funding rates and crowding signals before leveraged-position decisions for $0.004 USDC per request on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perria080925-bot](https://clawhub.ai/user/perria080925-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Crypto analysts and agent developers use this skill to compare current perpetual funding rates across assets and venues and assess positioning before considering leveraged trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A wallet-enabled agent may make paid requests without explicit confirmation or spending limits.

Mitigation: Require approval for each request, verify the $0.004 USDC charge on Base and the expected endpoint, and set a small session budget or dry-run mode where possible.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/perria080925-bot/skills/crypto-funding-heatmap)
- [Funding heatmap API endpoint](https://x402.bankr.bot/0xf436ca41bd0a236338bef57adeb4976677513010/funding-heatmap)

## Skill Output:

**Output Type(s):** [Analysis, API calls, Shell commands]

**Output Format:** [Markdown guidance and JSON API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Point-in-time rates, annualized extremes, crowding flags and data sources; paid requests cost $0.004 USDC on Base.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
