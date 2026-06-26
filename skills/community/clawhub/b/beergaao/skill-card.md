## Description: <br>
A股/港股/美股量化分析工具，提供技术分析、策略生成、回测验证和风险管理功能。 <br>

This skill is for research and development only. <br>

## Publisher: <br>
[ganjiakoun16](https://clawhub.ai/user/ganjiakoun16) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and financial-analysis teams use this skill to equip agents with stock-market data access, technical analysis, strategy generation, backtesting, and risk-management guidance for A-share, Hong Kong, and U.S. equities. Its outputs should be treated as research support rather than investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags the release for review because it creates an optional brokerage trading context while describing itself as data-only and non-trading. <br>
Mitigation: Use read-only market-data credentials, avoid brokerage tokens with trading permissions, and review Longport-related behavior before use. <br>
Risk: Trading signals and backtest results may be incorrect, misleading, or unsuitable for a particular investment decision. <br>
Mitigation: Treat outputs as research support rather than investment advice and require independent review before any financial action. <br>
Risk: The skill may persist local SQLite data or model artifacts during analysis. <br>
Mitigation: Run in a virtual environment and review, restrict, or disable local database and model persistence as needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ganjiakoun16/beergaao) <br>
- [README](artifact/README.md) <br>
- [Factor reference](artifact/factor-reference.md) <br>
- [Risk and backtest reference](artifact/risk-reference.md) <br>
- [Strategy reference](artifact/strategy-reference.md) <br>
- [Tushare token registration](https://tushare.pro/register) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, Python snippets, shell commands, and JSON tool responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires market-data credentials such as TUSHARE_TOKEN; outputs may include stock signals, backtest metrics, risk checks, and local state updates.] <br>

## Skill Version(s): <br>
3.3.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
