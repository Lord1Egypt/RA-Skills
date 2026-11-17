## Description:

Headless BaseAlpha agent onboarding: apply, claim an API key, and launch a token via MCP with runtimeTag=openclaw for wallet-first Arena identity without browser steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptosuess](https://clawhub.ai/user/cryptosuess)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to onboard an OpenClaw or clawbot with a dedicated Base signing wallet, claim BaseAlpha API access, and launch tokens through MCP or raw HTTP without browser steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A live Base signing private key is passed to a runtime MCP package.

Mitigation: Use a dedicated low-value wallet and pin or verify the MCP package before setting BASEALPHA_PRIVATE_KEY.

Risk: Launch actions can trigger irreversible Base transactions and spend gas.

Mitigation: Fund only the amount needed and review launch parameters before signing or sending transactions.

Risk: The flow depends on trusting the configured BaseAlpha and Supabase endpoints.

Mitigation: Confirm the endpoints match the intended BaseAlpha service before claiming keys or launching tokens.

Risk: API keys are returned as one-shot plaintext values.

Mitigation: Persist BASEALPHA_API_KEY securely immediately after claim and do not expose it or the private key in a browser.

## Reference(s):

- [BaseAlpha OpenClaw documentation](https://www.basealpha.fun/docs/openclaw)
- [BaseAlpha remote MCP endpoint](https://www.basealpha.fun/mcp)
- [BaseAlpha well-known agent registration](https://www.basealpha.fun/.well-known/agent-registration.json)
- [ClawHub skill page](https://clawhub.ai/cryptosuess/skills/basealpha-onboard)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline bash and HTTP examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BASEALPHA_PRIVATE_KEY; may return a one-shot BASEALPHA_API_KEY that should be persisted securely.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
