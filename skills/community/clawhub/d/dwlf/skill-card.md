## Description:

Interact with DWLF, a market analysis platform for crypto and stocks, through market data, chart indicators, strategy, backtesting, portfolio, trade journaling, and academy workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andywilliams](https://clawhub.ai/user/andywilliams)

### License/Terms of Use:

MIT

## Use Case:

ClawHub and Clawdbot users use this skill to let an agent retrieve DWLF market analysis, inspect trading signals, build and backtest strategies, manage watchlists and journals, and summarize account-level market context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A real DWLF API key can grant access to account data and trading-related resources.

Mitigation: Use a narrowly scoped, expiring API key stored in an environment variable or secrets manager.

Risk: The API wrapper can send the API key to a host configured through DWLF_API_URL.

Mitigation: Leave DWLF_API_URL unset unless the destination is explicitly trusted.

Risk: The skill exposes create, update, delete, compile, purge, and activation workflows for trading-related resources.

Mitigation: Require explicit user confirmation before any write, delete, compile, purge, or activation action.

## Reference(s):

- [DWLF API Endpoints Reference](artifact/references/api-endpoints.md)
- [DWLF Strategy Builder Reference](artifact/references/strategy-builder.md)
- [DWLF Website](https://dwlf.co.uk)
- [DWLF API](https://api.dwlf.co.uk/v2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, shell commands, and JSON API request or response payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and a DWLF API key for authenticated account actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
