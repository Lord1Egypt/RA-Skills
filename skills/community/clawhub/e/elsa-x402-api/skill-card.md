## Description:

DeFi tools for portfolio analysis, token search, and swap execution via Elsa API with x402 micropayments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justjkk](https://clawhub.ai/user/justjkk)

### License/Terms of Use:

MIT

## Use Case:

Developers and external OpenClaw users use this skill to query DeFi portfolio and token data, inspect wallet risk, request swap quotes, and run transaction workflows when execution is explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can sign wallet transactions and x402 payments.

Mitigation: Use a low-balance payment wallet, keep a separate low-balance TRADE_PRIVATE_KEY for execution, and enable transaction tools only when needed.

Risk: The local_signer mode depends on trusting the transaction data returned by the Elsa API.

Mitigation: Avoid local_signer unless the API response is independently trusted; otherwise review transaction data or use an external signing flow.

Risk: Documented budget limits should not be treated as hard protection.

Mitigation: Monitor budget status, keep wallets low balance, and review spending before repeated paid API calls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justjkk/skills/elsa-x402-api)
- [Elsa API](https://x402.heyelsa.ai)
- [x402 Protocol](https://x402.org)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Structured JSON responses and Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PAYMENT_PRIVATE_KEY for x402 payments; transaction execution is opt-in and can use a separate TRADE_PRIVATE_KEY.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
