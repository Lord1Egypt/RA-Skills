## Description:

AI agent skill for Alpaca Markets trading, including guided setup, stock and crypto trading commands, portfolio management, order execution, and paper trading by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zijunl](https://clawhub.ai/user/zijunl)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and agent operators use this skill to let an AI agent interact with Alpaca Markets through a Python CLI for account checks, market status, quotes, portfolio review, and order workflows. Setup requires user-controlled Alpaca credentials and should start with paper-trading keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables high-impact financial trading workflows through an agent.

Mitigation: Start with Alpaca paper-trading keys, review account state and orders before execution, and avoid live-trading credentials unless the user understands the financial impact.

Risk: API keys may be stored persistently in shell startup files and exposed to agents or local processes.

Mitigation: Complete credential entry in a trusted session, use least-privilege keys where possible, protect shell profile files, and rotate keys if they appear in an untrusted transcript or profile.

Risk: Setup may modify shell configuration and has consent-sensitive steps.

Mitigation: Require explicit user consent before credential setup or shell profile changes, and let the user perform registration, email verification, and API key generation directly when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zijunl/skills/alpaca-py-cli)
- [Alpaca Markets](https://alpaca.markets)
- [Alpaca Python SDK documentation](https://alpaca.markets/docs/python-sdk/)
- [Alpaca API reference](https://docs.alpaca.markets/reference/)
- [Alpaca Trading API documentation](https://docs.alpaca.markets/docs/trading-api)
- [Alpaca Market Data API documentation](https://docs.alpaca.markets/docs/market-data)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide credential setup and trading actions; users should review commands before execution.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
