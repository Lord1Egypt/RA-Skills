## Description: <br>
Provides A-share real-time quote lookup, intraday volume analysis, main-fund movement signals, limit-up order checks, and local portfolio profit and loss management for Shanghai, Shenzhen, and Beijing exchange stocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query China A-share market quotes, inspect intraday volume distribution, identify documented volume-signal patterns, and manage a simple local portfolio record. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Quote analysis sends requested stock symbols to Sina Finance. <br>
Mitigation: Use only symbols that are acceptable to disclose to the external quote service. <br>
Risk: Portfolio add, update, and remove commands immediately edit the local portfolio file. <br>
Mitigation: Review command arguments before execution and keep backups of important local portfolio data. <br>
Risk: Market data and volume-signal analysis can be delayed or incomplete and should not be treated as financial advice. <br>
Mitigation: Validate important decisions against trusted financial data sources and human review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/litiao1224/a-stock-analysis-bak) <br>
- [Sina Finance](https://finance.sina.com.cn) <br>
- [Sina real-time quote endpoint](https://hq.sinajs.cn/list={codes_str}) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Command-line text tables and optional JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write and update a local portfolio JSON file under the user's home directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
