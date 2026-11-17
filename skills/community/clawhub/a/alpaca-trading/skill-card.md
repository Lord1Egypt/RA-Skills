## Description:

Trade stocks, ETFs, options, and crypto through Alpaca's REST API using curl, including order management, portfolio/account review, watchlists, account activities, corporate actions, and real-time or historical market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lacymorrow](https://clawhub.ai/user/lacymorrow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to retrieve Alpaca account and market information, prepare order requests, and manage Alpaca orders, positions, watchlists, options contracts, and related trading workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place trades, exercise options, cancel orders, close positions, and change account configuration when given valid Alpaca credentials.

Mitigation: Use paper-trading keys by default, keep live keys separate, and require explicit human approval before any order, option exercise, cancellation, account-configuration change, or position close.

Risk: Misconfigured API endpoints can send requests to the wrong Alpaca environment.

Mitigation: Verify APCA_API_BASE_URL and APCA_DATA_API_BASE_URL before each session, especially before enabling live trading.

Risk: Broad cancel-all and close-all operations can affect many orders or positions at once.

Mitigation: Require the agent to show the exact request and obtain human confirmation before running cancel-all or close-all commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lacymorrow/skills/alpaca-trading)
- [Alpaca REST API reference](references/api.md)
- [Alpaca](https://alpaca.markets)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Alpaca API credentials in environment variables and uses paper trading by default unless the live trading endpoint is explicitly configured.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
