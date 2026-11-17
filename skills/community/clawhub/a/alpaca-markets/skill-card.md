## Description:

This skill provides integration with the Alpaca Markets API for trading stocks, options, and cryptocurrencies, including account queries, order management, positions, and market data access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oscraters](https://clawhub.ai/user/oscraters)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to interact with Alpaca Markets brokerage services through authenticated REST API calls for paper or live trading workflows. It is suited for account inspection, order placement and management, position management, and market data retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use brokerage credentials for live account-changing actions, including placing orders, canceling orders, and closing positions.

Mitigation: Use paper-trading credentials first, and provide live credentials only after code review and explicit approval for live trading.

Risk: A configurable ALPACA_BASE_URL can send credentials to an unintended endpoint if set incorrectly.

Mitigation: Leave ALPACA_BASE_URL unset by default, or set it only to an official Alpaca URL that has been verified.

Risk: Bulk cancel and close-all-position calls can materially affect an account.

Mitigation: Require explicit human confirmation before running bulk cancel or close-all-position operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oscraters/skills/alpaca-markets)
- [ClawHub distribution page](https://clawhub.ai/oscraters/alpaca-markets)
- [OpenClaw metadata source repository](https://github.com/oscraters/alpaca-markets-skill.git)
- [Alpaca Markets API Reference](references/api_reference.md)
- [Alpaca documentation](https://docs.alpaca.markets/)

## Skill Output:

**Output Type(s):** [API calls, shell commands, configuration, guidance, text]

**Output Format:** [Markdown guidance with inline shell commands and JSON or text API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ALPACA_API_KEY and ALPACA_API_SECRET; ALPACA_BASE_URL optionally selects the Alpaca API environment.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
