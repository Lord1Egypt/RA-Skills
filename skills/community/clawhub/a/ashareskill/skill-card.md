## Description: <br>
Ashareskill uses BaoStock to fetch A-share K-line market data and calculate technical indicators for individual stocks, stock pools, and supported index constituents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caoyachao](https://clawhub.ai/user/caoyachao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent workflows use this skill to retrieve BaoStock A-share historical K-line data, calculate indicators such as MA, MACD, KDJ, RSI, BOLL, and CCI, and export the results for quantitative analysis or backtesting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market data fetched over the network may be unavailable, delayed, or unsuitable as investment advice. <br>
Mitigation: Use the output for analysis only and verify data before relying on it for financial decisions. <br>
Risk: Dependency versions can affect reproducibility of fetched data processing and indicator calculations. <br>
Mitigation: Install the skill in a virtual environment and pin or review dependency versions when reproducibility matters. <br>
Risk: CSV outputs are written to user-selected paths and can clutter or overwrite local analysis files. <br>
Mitigation: Save outputs in a dedicated folder and review the target path before running batch exports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caoyachao/ashareskill) <br>
- [BaoStock data source](http://baostock.com/) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Code, CSV files, Analysis] <br>
**Output Format:** [Console text and CSV files, with Python DataFrame objects when used as a module] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches market data over the network and saves user-requested CSV outputs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
