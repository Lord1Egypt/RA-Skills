## Description: <br>
A股量化工具包 helps an agent retrieve market data, calculate technical indicators, run backtests, monitor scores, perform FFT analysis, and generate A-share market reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dnaxxx-hub](https://clawhub.ai/user/dnaxxx-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and finance-focused agents use this skill to analyze A-share market data, compare trading strategies, run parameter searches, monitor technical signals, and produce concise market reports. Outputs are analytical aids and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence marks the release suspicious because some modules contain hidden automatic execution paths. <br>
Mitigation: Review the skill before installing or running it, and remove or explicitly document hidden execution paths before use in managed environments. <br>
Risk: The skill performs expected market-data network access and may optionally forward alerts. <br>
Mitigation: Run it in a network policy appropriate for market-data access, and make alert forwarding explicit and opt-in before deployment. <br>
Risk: Backtests, scores, and strategy signals can be mistaken for reliable trading advice. <br>
Mitigation: Treat generated analysis as decision support only, validate data quality independently, and require human review before any trading action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dnaxxx-hub/finance-toolkit) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with Python examples, shell commands, tables, and generated report content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live market data, backtest metrics, technical indicators, monitoring alerts, and generated daily-report summaries.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
