## Description:

Provides a Python client for querying Futu brokerage positions, account information, orders, deals, watchlists, and market data, and for placing or modifying orders through Futu OpenAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xdl2003](https://clawhub.ai/user/xdl2003)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading automation users can use this skill to integrate a local FutuOpenD session with agent workflows that inspect account state, retrieve market data, and prepare brokerage actions. Use live trading methods only with explicit human confirmation and order limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read brokerage account data and submit real orders through a running FutuOpenD session.

Mitigation: Use SIMULATE explicitly for testing, keep trading passwords out of logs and shared prompts, and require human confirmation before any live order action.

Risk: Live trading can create real financial loss if an agent calls order methods without limits.

Mitigation: Set account-level and workflow-level order limits, restrict access to live trading methods, and review price, quantity, side, symbol, and environment before submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xdl2003/skills/futu-client)
- [Publisher profile](https://clawhub.ai/user/xdl2003)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and shell examples, plus Python client methods returning dictionaries or pandas DataFrames]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a running local FutuOpenD service and futu-api dependency; brokerage methods may access account data and submit real orders.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
