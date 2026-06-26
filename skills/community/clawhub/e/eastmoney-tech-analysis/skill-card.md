## Description: <br>
Provides Chinese stock K-line data retrieval, KDJ, MACD, BOLL, and MA technical indicators, capital-flow rankings, and summarized buy/sell signal analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zaferliu](https://clawhub.ai/user/zaferliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to retrieve Eastmoney market data, compute common technical indicators, inspect capital-flow rankings, and generate text or JSON technical-analysis reports for Chinese stock symbols. Outputs are informational and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependencies are declared with lower bounds rather than pinned or locked versions. <br>
Mitigation: Install in an isolated environment, pin or lock dependency versions before production use, and run dependency scanning in the target environment. <br>
Risk: Market data and technical indicators can be delayed, incomplete, or unavailable from the upstream data service. <br>
Mitigation: Validate important outputs against a trusted market-data source before relying on them for decisions. <br>
Risk: Technical-analysis reports and buy/sell signal summaries may be mistaken for financial advice. <br>
Mitigation: Present outputs as informational analysis only and require human financial review before any trading or investment action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zaferliu/eastmoney-tech-analysis) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Code, Shell commands, Guidance] <br>
**Output Format:** [Plain text reports, JSON objects, Python examples, and command-line usage snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include market data, calculated indicators, trading-signal summaries, and risk notices.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
