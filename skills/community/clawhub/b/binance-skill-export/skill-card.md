## Description:

Provides Binance API integration for spot and futures trading, including balance checks, market data, order management, leverage settings, and position management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ly5201314gjx](https://clawhub.ai/user/ly5201314gjx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading operators use this skill to let an agent query Binance spot and futures account information, inspect market data, place or review orders, set leverage, and close futures positions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place live spot or futures orders.

Mitigation: Use a dedicated least-privilege Binance API key, prefer read-only or testnet keys where possible, and require separate human confirmation before any order function is called.

Risk: The skill can change futures leverage and close futures positions.

Mitigation: Restrict key permissions and IPs, set explicit operational limits outside the skill, and require human approval before leverage or close-position actions.

Risk: API credentials are required for account and trading actions.

Mitigation: Provide credentials only through environment variables, never hardcode secrets in source, and rotate or revoke keys if exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ly5201314gjx/skills/binance-skill-export)
- [Publisher Profile](https://clawhub.ai/user/ly5201314gjx)
- [Binance Spot API Endpoint](https://api.binance.com)
- [Binance Futures API Endpoint](https://fapi.binance.com)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration]

**Output Format:** [Plain text responses with JavaScript examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BINANCE_API_KEY and BINANCE_SECRET_KEY environment variables; functions may call live Binance spot and futures endpoints.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
