## Description:

Binance Alpha new coin launch detector. Uses WebSocket to monitor !miniTicker@arr stream and detects new trading pairs immediately when they appear. Maintains known symbols set in memory and triggers alert for new symbols with valid opening price.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manifoldor](https://clawhub.ai/user/manifoldor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-monitoring users use this skill to run a Binance public-market monitor that watches spot ticker streams for newly appearing trading pairs and reviews recent listing alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The monitor is long-lived and stores symbol baselines and alert history in the user's home directory.

Mitigation: Run it only in a trusted local environment and review or remove ~/.config/alpha state files when they are no longer needed.

Risk: The skill depends on websocket-client from the Python package ecosystem.

Mitigation: Use a virtual environment and pin websocket-client to a reviewed version before running the monitor.

Risk: Listing alerts can be affected by network instability, API availability, and market-data timing.

Mitigation: Treat alerts as signals to verify against Binance or another trusted market source before acting on them.

## Reference(s):

- [Binance WebSocket API](https://binance-docs.github.io/apidocs/spot/en/#websocket-market-streams)
- [Binance REST API](https://api.binance.com/api/v3)
- [miniTicker Docs](references/binance_ws.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and terminal output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime script writes known-symbol and alert-history JSON files under ~/.config/alpha.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
