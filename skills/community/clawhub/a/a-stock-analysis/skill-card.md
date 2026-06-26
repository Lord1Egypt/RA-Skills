## Description: <br>
提供A股实时行情、分时成交量分布及主力资金动向分析，支持持仓管理和盈亏监控。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CNyezi](https://clawhub.ai/user/CNyezi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Investors, analysts, and agents use this skill to query A-share market data, inspect intraday volume distribution, identify heuristic capital-flow signals, and track local portfolio profit and loss. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio commands store and modify local holding details on disk. <br>
Mitigation: Review add, update, and remove commands before running them and keep the local portfolio file protected. <br>
Risk: Queried stock codes are sent to Sina Finance to retrieve market data. <br>
Mitigation: Use the skill only when sending those stock codes to the external data source is acceptable. <br>


## Reference(s): <br>
- [Sina Finance](https://finance.sina.com.cn) <br>
- [Sina Finance realtime quote endpoint](https://hq.sinajs.cn/list={codes_str}) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Plain text analysis, optional JSON, and local portfolio JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries Sina Finance market data and stores portfolio details locally when portfolio commands are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
