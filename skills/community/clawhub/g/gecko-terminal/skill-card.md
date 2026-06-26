## Description: <br>
Query GeckoTerminal market data for networks, DEXes, pools, tokens, OHLCV, trades, and trending or new pools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BRS999](https://clawhub.ai/user/BRS999) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to retrieve read-only GeckoTerminal market data through a local Node CLI for discovery, pool analysis, token lookup, OHLCV review, and automation-friendly JSON outputs. Market data should be treated as informational rather than trading advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake public market data for trading advice. <br>
Mitigation: Treat all returned market data as informational and review it before making financial decisions. <br>
Risk: Network, token, pool, and search-query values are sent to GeckoTerminal's public API. <br>
Mitigation: Avoid submitting sensitive or private identifiers in query values and use the skill only when public API disclosure is acceptable. <br>


## Reference(s): <br>
- [GeckoTerminal homepage](https://www.geckoterminal.com) <br>
- [GeckoTerminal API v2](https://api.geckoterminal.com/api/v2) <br>
- [ClawHub skill page](https://clawhub.ai/BRS999/gecko-terminal) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [JSON responses from a Node CLI, with Markdown command examples in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are read-only GeckoTerminal public API responses suitable for piping and automation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
