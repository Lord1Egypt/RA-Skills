## Description: <br>
Provides Python tools for China A-share market data retrieval, technical indicators, strategy backtesting, monitoring scores, FFT analysis, and daily report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dnaxxx-hub](https://clawhub.ai/user/dnaxxx-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-analysis users can use this skill to fetch A-share market data, run technical-analysis and backtesting workflows, monitor selected stocks, and generate market reports. Treat generated buy, sell, scoring, and alert outputs as educational analysis aids, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market-data lookups and generated reports may create local cache or report files. <br>
Mitigation: Run the tool in a workspace where local generated files are expected, and review generated reports before sharing them. <br>
Risk: Generated buy, sell, score, and alert outputs may be mistaken for investment advice. <br>
Mitigation: Present outputs as educational signals only and require independent financial review before any trading decision. <br>
Risk: Security evidence notes under-disclosed process handoff and alert synchronization behavior. <br>
Mitigation: Review the relevant scripts before direct execution and disable host knowledge-bridge integrations unless they are explicitly intended. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dnaxxx-hub/a-stock-quant-toolkit) <br>
- [Artifact README](README.md) <br>
- [Artifact skill documentation](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell examples; runtime helpers may return dictionaries, tabular analysis, generated reports, plots, and JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch public market data, write local cache and report files, and produce trading signals, scoring output, alerts, and strategy-analysis summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, finance_toolkit/__init__.py) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
