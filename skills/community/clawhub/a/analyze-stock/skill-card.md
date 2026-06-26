## Description: <br>
股票分析技能，提供买卖点判断、仓位管理、基本面分析。使用当用户需要分析股票投资价值时。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zxsadc2025](https://clawhub.ai/user/zxsadc2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze stock investment value from a stock code, combining financial data, valuation zones, position management guidance, fundamentals, and market/news signals into a structured report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real-looking API keys appear in documentation history or release notes. <br>
Mitigation: Review the package before installation, rotate any exposed credentials, and use only user-owned scoped API keys supplied through environment variables. <br>
Risk: Stock symbols and company queries may be sent to Tushare, Baidu, Tavily, and the configured LLM provider. <br>
Mitigation: Treat requested symbols and company names as outbound data, and install only where those external data flows are acceptable. <br>
Risk: External search helper execution may receive broad environment access. <br>
Mitigation: Prefer a cleaned package that narrows helper subprocess environment variables and declares all required external services. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zxsadc2025/analyze-stock) <br>
- [Tushare](https://tushare.pro) <br>
- [Tavily](https://tavily.com) <br>
- [Fundamental Analysis Framework](references/fundamental_analysis.md) <br>
- [Position Management](references/position_management.md) <br>
- [Valuation Zones](references/valuation_zones.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON containing a Markdown stock analysis report and model-generated opportunity and risk analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and user-provided TUSHARE_TOKEN; BAIDU_API_KEY and TAVILY_API_KEY support optional news and deeper analysis flows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
