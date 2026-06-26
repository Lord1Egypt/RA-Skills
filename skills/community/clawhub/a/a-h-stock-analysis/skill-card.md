## Description: <br>
A股和港股股票数据分析工具，优先使用Tushare数据，Tushare不可用时自动回退到AKShare获取行情、财务指标，支持基本面分析和技术分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zh40](https://clawhub.ai/user/zh40) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to fetch A-share and Hong Kong stock data, inspect basic company information, review financial indicators, and calculate technical indicators. It supports Tushare when configured and falls back to AKShare when Tushare is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to Tushare or AKShare for market data. <br>
Mitigation: Run it in an environment where network access to those providers is expected and permitted. <br>
Risk: A TUSHARE_TOKEN may be used when configured. <br>
Mitigation: Set TUSHARE_TOKEN only in trusted environments and avoid exposing it in shared shells, logs, or committed files. <br>
Risk: Commands with --output can write CSV files to user-supplied paths. <br>
Mitigation: Review output paths before execution and prefer a dedicated working directory for generated CSV files. <br>


## Reference(s): <br>
- [Tushare API 常用接口](references/tushare-api.md) <br>
- [Tushare](https://tushare.pro/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Command-line text output with optional CSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a TUSHARE_TOKEN environment variable when available; otherwise falls back to AKShare public data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
