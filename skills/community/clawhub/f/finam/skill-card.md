## Description:

Execute trades, manage portfolios, access real-time market data, browse and search market assets, scan volatility, and answer questions about Finam Trade API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexander-panov](https://clawhub.ai/user/alexander-panov)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, trading operators, and analysts use this skill to interact with the Finam Trade API for market data, portfolio checks, asset discovery, volatility scans, and user-confirmed order workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place or cancel live brokerage orders.

Mitigation: Require explicit user confirmation of symbol, side, quantity, order type, and price before any order or cancellation.

Risk: Finam credentials and JWTs can expose access to a real brokerage account.

Mitigation: Use the least-privileged API key available and keep FINAM_API_KEY, FINAM_ACCOUNT_ID, and FINAM_JWT_TOKEN out of logs and chat transcripts.

Risk: The gRPC workflow installs FinamPy from an unpinned Git URL.

Mitigation: Pin and review the FinamPy dependency before enabling the gRPC workflow.

Risk: Live market data, account data, and volatility scans may be incomplete, stale, rate-limited, or unavailable.

Mitigation: Treat outputs as decision-support information and verify account state, prices, and orders with Finam before acting.

## Reference(s):

- [Finam Trade API](https://tradeapi.finam.ru/)
- [REST Reference](references/REST.md)
- [gRPC Python Reference](references/GRPC.md)
- [Finam API Token Documentation](https://tradeapi.finam.ru/docs/tokens)
- [Finam Skill on ClawHub](https://clawhub.ai/alexander-panov/skills/finam)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with shell and Python code blocks plus JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Finam credentials for live API workflows and can produce commands that interact with brokerage account data or orders.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
