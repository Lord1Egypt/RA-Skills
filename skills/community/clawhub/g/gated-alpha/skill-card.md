## Description:

Discover, filter, and purchase structured crypto alpha calls from Gated Alpha. Supports push delivery via webhooks (recommended) or direct polling. Pay-per-call via x402 on Base (USDC). Owner payouts fire onchain within seconds of each purchase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zich-agent](https://clawhub.ai/user/zich-agent)

### License/Terms of Use:


## Use Case:

External agents and developers use this skill to subscribe to or poll Gated Alpha crypto calls, evaluate previews, and purchase selected full payloads through x402 USDC payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook requests could trigger USDC purchases without clear authentication or spending controls.

Mitigation: Require signed or secret-authenticated webhooks, validate subscription and alpha IDs, and enforce per-purchase and daily USDC limits.

Risk: Wallet private keys and funded wallets are exposed to payment-flow risk.

Mitigation: Use a dedicated low-balance wallet and keep private keys outside source code.

Risk: A received paid URL could direct the agent into unintended purchases.

Mitigation: Construct purchase URLs locally or allowlist the exact Gated Alpha origin before payment.

Risk: Automatic buying can spend funds on low-quality or unwanted alpha.

Mitigation: Require manual approval unless automatic buying is intentionally enabled with tight limits and filtering.

## Reference(s):

- [Gated Alpha Skill on ClawHub](https://clawhub.ai/zich-agent/skills/gated-alpha)
- [zich-agent Publisher Profile](https://clawhub.ai/user/zich-agent)
- [Gated Alpha Live API](https://www.gatedalpha.xyz)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Code, Configuration]

**Output Format:** [Markdown with HTTP, JSON, and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes webhook and polling flows, x402 purchase examples, filtering guidance, subscription management, and payment constants.]

## Skill Version(s):

3.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
