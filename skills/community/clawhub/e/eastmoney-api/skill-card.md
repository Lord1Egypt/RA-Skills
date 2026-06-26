## Description: <br>
Eastmoney Api helps VAlpha quant-terminal users fetch A-share market data, switch among Eastmoney, Tushare, and Akshare data sources, and apply rate limits and circuit-breaker handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative-finance practitioners use this skill to generate or guide data-fetching, analysis, and backtesting workflows for China A-share strategies. It can also guide related VAlpha application flows such as market-data endpoints, portfolio analysis, reports, and scheduled jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill label emphasizes Eastmoney market data, but the referenced instructions cover broader finance-application behavior including auth, admin, LLM, portfolio, scheduling, and server workflows. <br>
Mitigation: Review the full capability catalog before installation and approve server startup, scheduled jobs, generated trading code, or new skill creation only when those workflows are intended. <br>
Risk: Finance workflows may involve sensitive credentials, paid API keys, broker connections, or live financial accounts. <br>
Mitigation: Run in a virtual environment, provide only the credentials required for the intended data source, and do not connect broker credentials or live accounts without explicit approval. <br>
Risk: External financial data providers may enforce rate limits or block clients after excessive retries. <br>
Mitigation: Use configured rate limits, HTTP timeouts, and provider fallback behavior, and stop retries during provider blocks. <br>


## Reference(s): <br>
- [Eastmoney Api ClawHub release](https://clawhub.ai/tangweigang-jpg/eastmoney-api) <br>
- [Human Summary](human_summary.md) <br>
- [Known Use Cases](references/USE_CASES.md) <br>
- [Semantic Locks](references/LOCKS.md) <br>
- [Constraints](references/CONSTRAINTS.md) <br>
- [Component Capability Map](references/COMPONENTS.md) <br>
- [Anti-Patterns](references/ANTI_PATTERNS.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with inline code and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request market, data provider, strategy type, date range, and target entity IDs before producing implementation guidance.] <br>

## Skill Version(s): <br>
0.3.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
