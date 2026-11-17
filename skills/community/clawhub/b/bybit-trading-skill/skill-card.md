## Description:

Unofficial Bybit AI trading skill - trade on Bybit using natural language, covering spot, derivatives, earn, and related workflows with Bybit API credentials and explicit confirmation for real-money writes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bybit-exchange-ops](https://clawhub.ai/user/bybit-exchange-ops)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an AI assistant to check Bybit markets, manage account information, and prepare or execute Bybit trading operations across spot, derivatives, earn, bots, copy trading, and related modules. It requires Bybit API credentials and explicit confirmation for mainnet write operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live Bybit Read+Trade credentials can authorize real-money account actions.

Mitigation: Use testnet first, keep funds in a dedicated limited-balance sub-account, never enable withdrawals, bind keys to an IP when possible, and review each mainnet confirmation card before typing CONFIRM.

Risk: The release has no server-resolved GitHub import provenance and is not proven to be official Bybit software.

Mitigation: Treat it as a third-party community skill, review the bundled source before installation, and avoid connecting mainnet credentials until the package is trusted.

Risk: API secrets may be exposed if stored or displayed carelessly.

Mitigation: Prefer a secure secret store over .env or shell profile files and keep credentials out of conversations, logs, generated code, and command output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bybit-exchange-ops/skills/bybit-trading-skill)
- [Bybit](https://www.bybit.com)
- [Bybit API management](https://www.bybit.com/app/user/api-management)
- [Bybit TradFi Integration docs](https://bybit-exchange.github.io/docs/v5/tradfi-integration)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown with inline shell commands, code snippets, configuration examples, structured confirmation cards, and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BYBIT_API_KEY and BYBIT_API_SECRET; BYBIT_ENV defaults to testnet; mainnet write operations require explicit user confirmation.]

## Skill Version(s):

1.2.7 (source: server release evidence, skill frontmatter, and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
