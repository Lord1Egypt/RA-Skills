## Description: <br>
BitSoulStockSkill helps agents answer A-share market questions with stock screening strategies, quantitative indicators, MOE factor signals, risk checks, backtesting, historical market data, sector data, transaction data, and trader-observation summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzhi43](https://clawhub.ai/user/wangzhi43) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query and analyze China A-share market data, run stock screening and backtesting workflows, and produce stock reports with indicators, risk notes, and trading-signal context. Outputs should be treated as informational analysis rather than financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flagged the release as suspicious because remote data-package updates and token handling need review before installation. <br>
Mitigation: Install only if the BitSoul/aicodingyard service is trusted, use a limited token, keep token env files private, and consider an isolated BITSOUL_CACHE_DIR. <br>
Risk: Remote update, training, or data-fetch workflows can change local data used by analysis. <br>
Mitigation: Avoid automatic update and training calls unless the data source and cache location have been reviewed. <br>
Risk: Buy, sell, and trade-signal outputs may be mistaken for financial advice. <br>
Mitigation: Treat outputs as informational and review them independently before making investment decisions. <br>


## Reference(s): <br>
- [StockApi API reference](references/API_FOR_LLM.md) <br>
- [BitSoul homepage](https://www.aicodingyard.com) <br>
- [Sina Finance](https://finance.sina.com.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Simplified Chinese reports, Markdown tables, and structured JSON returned from stock-analysis APIs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses BITSOUL_TOKEN for remote data access and may read an explicitly configured token env file.] <br>

## Skill Version(s): <br>
1.0.31 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
