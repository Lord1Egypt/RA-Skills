## Description: <br>
Data Hub provides an asynchronous in-memory data sharing layer for multi-agent quantitative trading systems, organizing market state, indicators, intelligence, and risk-audit state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnny-ggao](https://clawhub.ai/user/johnny-ggao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to share validated market, indicator, intelligence, and risk-audit data across trading-system agents. It is for shared context and status retrieval, not persistent history, market-data sourcing, or direct trade execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Risk-audit snapshots can persist sensitive risk data to disk when snapshot_path or snapshot helpers are used. <br>
Mitigation: Avoid sensitive account details, constrain snapshot locations at the application layer, and review or patch snapshot functions before use in a trading environment. <br>


## Reference(s): <br>
- [Data Hub Skill Documentation](docs/Data_Hub_Skill.md) <br>
- [Data Hub on ClawHub](https://clawhub.ai/johnny-ggao/data-hub) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Guidance] <br>
**Output Format:** [Structured JSON-compatible dictionaries with concise text error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes market_state, indicators, intelligence, and risk_audit namespaces; summary access may mark stale market data and expired intelligence.] <br>

## Skill Version(s): <br>
1.0.0 (source: pyproject.toml and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
