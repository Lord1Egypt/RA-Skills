## Description: <br>
Queries Chinese financial market and macroeconomic data through AKShare, including A-shares, indices, futures, funds, bonds, foreign exchange, and cryptocurrency prices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grandpaniu-fandougarden](https://clawhub.ai/user/grandpaniu-fandougarden) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and finance-focused agents use this skill to run AKShare-backed Python queries and summarize live or historical market, fund, bond, macroeconomic, foreign-exchange, and cryptocurrency data for users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live financial data may be incomplete, stale, or different from other market data providers. <br>
Mitigation: Treat results as informational and verify important figures with an authoritative source before relying on them. <br>
Risk: The broad finance trigger may activate for general finance questions where a live data query is not needed. <br>
Mitigation: Confirm the requested market, instrument, data type, and time range before running a query when the user's intent is ambiguous. <br>
Risk: Outputs could be mistaken for investment advice. <br>
Mitigation: Present queried data with source and timing context and avoid making financial recommendations from the returned values alone. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/grandpaniu-fandougarden/finance-query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON from the query script, typically summarized as Markdown or text by the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live results depend on AKShare and upstream third-party data sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
