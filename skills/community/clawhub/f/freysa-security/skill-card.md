## Description:

On-chain security intelligence for autonomous agents - token honeypot detection, wallet forensics, pre-trade risk checks, CAPTCHA solving, and market data across 27 x402 pay-per-call endpoints on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayrecko](https://clawhub.ai/user/jayrecko)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and autonomous-agent builders use this skill to check token, wallet, approval, and transaction risk before interacting with Base network assets, and to call related paid intelligence, market-data, web-fetching, and CAPTCHA endpoints when authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CAPTCHA-solving endpoints can be misused if applied to challenges the user is not authorized to solve.

Mitigation: Use CAPTCHA solving only for authorized workflows and review policy requirements before enabling the endpoint for autonomous agents.

Risk: Setting FREYSA_WALLET_KEY can expose wallet and payment authority for x402 calls.

Mitigation: Avoid configuring FREYSA_WALLET_KEY unless the operator understands the wallet risk; prefer scoped wallets and manual payment review where appropriate.

Risk: Token, wallet, URL, and CAPTCHA inputs may be sent to Freysa and relevant backends when endpoints are used.

Mitigation: Do not submit sensitive data unless sharing it with the service and downstream providers is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jayrecko/skills/freysa-security)
- [Freysa Security x402 Manifest](https://economic-agent-369.freysa.dev/.well-known/x402)
- [Freysa Security Agent Card](https://economic-agent-369.freysa.dev/.well-known/agent-card.json)
- [Freysa Security OpenAPI Specification](https://economic-agent-369.freysa.dev/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with endpoint references, shell and Python examples, and API-specific response content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include paid x402 API call instructions and risk analysis derived from external Freysa endpoints.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
