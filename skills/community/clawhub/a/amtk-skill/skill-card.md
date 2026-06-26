## Description: <br>
AMtkSkill helps agents fetch A-share market data from Tushare, query local prices and valuations, and run technical analysis such as moving averages, RSI, MACD, Bollinger Bands, adjusted prices, and return statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lhkong7](https://clawhub.ai/user/lhkong7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, and agent operators use this skill to maintain a local A-share market dataset, inspect securities and valuation rankings, and generate technical-indicator summaries from command-line workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Tushare API token and makes outbound requests to Tushare. <br>
Mitigation: Store the token in the local environment configuration, avoid exposing it in prompts or logs, and review commands before execution. <br>
Risk: Large fetch operations can consume API quota and local disk space. <br>
Mitigation: Review date ranges, limits, batch size, and update scope before running fetch commands. <br>
Risk: Analyses depend on the freshness and completeness of the locally stored market data. <br>
Mitigation: Run the overview or update commands before relying on results, and treat indicator output as analytic support rather than financial advice. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lhkong7/amtk-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and tabular command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local file paths, stock symbols, date ranges, valuation metrics, and technical indicator values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
