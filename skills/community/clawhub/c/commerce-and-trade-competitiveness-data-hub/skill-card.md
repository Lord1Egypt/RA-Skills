## Description: <br>
Commerce and Trade Competitiveness Data Hub lets agents query World Bank TCdata360 trade and competitiveness data by country or region through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch trade, competitiveness, logistics, tariff, trade-cost, and regional comparison data for countries, regions, income groups, and global aggregates. It supports export market analysis, trade competitiveness benchmarking, tariff and logistics monitoring, cross-border policy research, and country trade profile comparisons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an external AgentPMT-hosted service and the action is listed at 5 credits per query. <br>
Mitigation: Confirm the AgentPMT service relationship and credit cost before installation or repeated use. <br>
Risk: Account secrets, wallet keys, signatures, or payment headers could be exposed if included in prompts or logs. <br>
Mitigation: Keep secrets and payment data out of prompts and logs, and use the referenced setup skills for credential handling. <br>
Risk: Endpoint details, schemas, setup steps, or examples may change after publication. <br>
Mitigation: Refresh the skill if it is more than 7 days past its listed update date and fetch live schema or instructions before production integrations. <br>
Risk: Queries can fail or return corrections when country, region, income group, or time-period inputs are unsupported or ambiguous. <br>
Mitigation: Use English country or region names within the documented limits, preserve failed request parameters, and retry only after fixing schema, authentication, payment, or input issues. <br>


## Reference(s): <br>
- [Commerce and Trade Competitiveness Data Hub marketplace page](https://www.agentpmt.com/marketplace/trade-competitiveness-data) <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/commerce-and-trade-competitiveness-data-hub) <br>
- [Action schema](artifact/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, JSON, API calls, text] <br>
**Output Format:** [Markdown instructions with JSON request and response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill defines one AgentPMT-hosted action, query_trade_data, with country_or_region required and optional trade topic, time period, trend, LPI, Doing Business, regional comparison, and trade balance controls.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
