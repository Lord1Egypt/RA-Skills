## Description:

Use AgentFuel to call Replicate, Anthropic, and ElevenLabs APIs using a single crypto-funded key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclawb17-stack](https://clawhub.ai/user/openclawb17-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to check AgentFuel balances, create USDT-funded invoices, transfer credits, and proxy AI API calls through AgentFuel to supported providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if real AgentFuel keys are placed in query-string URLs or prompts.

Mitigation: Use header-based authorization, avoid putting real keys in URLs or prompts, and rotate any key already used in a query-string URL.

Risk: Crypto-funded invoices and credit transfers can move value to the wrong network, recipient, or amount without enough guardrails.

Mitigation: Manually confirm invoice amount, token network, recipient key, and transfer amount before any payment or credit transfer.

## Reference(s):

- [ClawHub AgentFuel API Skill](https://clawhub.ai/openclawb17-stack/skills/agentfuel-api)
- [AgentFuel API Base URL](https://agentfuel.dev/v1)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENTFUEL_KEY for authenticated AgentFuel API calls.]

## Skill Version(s):

1.3.1 (source: server release metadata; artifact frontmatter lists 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
