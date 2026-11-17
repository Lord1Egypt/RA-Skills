## Description:

Generate AI images from text prompts. Pay per request with USDC on Solana via x402. No API keys, no accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geometrydotsh](https://clawhub.ai/user/geometrydotsh)

### License/Terms of Use:


## Use Case:

Developers and external agents use this skill to request priced AI image generation from text prompts through Geometry's x402 payment-enabled API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid generation requests spend USDC from a Solana wallet.

Mitigation: Use a dedicated low-balance wallet and verify the network, recipient, model price, and payment amount before signing.

Risk: Image prompts are sent to Geometry for processing.

Mitigation: Avoid submitting confidential, regulated, or sensitive prompt content unless approved for this third-party service.

Risk: The JavaScript quick start depends on npm packages for x402 and Solana payment handling.

Mitigation: Pin and review npm dependencies before use in production agent environments.

## Reference(s):

- [Geometry homepage](https://geometry.sh)
- [Geometry developer documentation](https://app.geometry.sh/developers)
- [Geometry agent card](https://api.geometry.sh/.well-known/agent.json)
- [x402 protocol](https://x402.org)
- [ClawHub skill page](https://clawhub.ai/geometrydotsh/skills/geometry)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions, API calls]

**Output Format:** [Markdown with JSON, JavaScript, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid generation requests return JSON with generation status, model, cost, and image URL.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
