## Description: <br>
Comprehensive guide for the FinLab quantitative trading package, covering data access, strategy development, backtesting, stock selection, factor analysis, and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[koreal6803](https://clawhub.ai/user/koreal6803) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and quantitative trading practitioners use this skill to build, backtest, analyze, and optionally prepare FinLab trading strategies using stock data, FinLabDataFrame, factor analysis, and broker workflow references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide broker credential handling and live order placement, which may expose accounts or create unintended trades. <br>
Mitigation: Use an isolated Python environment, keep credentials out of chats and source files, approve OAuth and broker logins manually, and require review of exact orders before execution. <br>
Risk: Backtest uploads may expose private strategy data. <br>
Mitigation: Keep private experiments set to upload=false unless the user deliberately opts in after reviewing what will be uploaded. <br>
Risk: Trading and backtesting outputs may be misleading or unsuitable for real financial decisions. <br>
Mitigation: Treat outputs as proposals, validate data sources, assumptions, code, and risk limits, and do not allow live trading without explicit human approval. <br>


## Reference(s): <br>
- [FinLab Skill Source](artifact/SKILL.md) <br>
- [Data Reference](artifact/data-reference.md) <br>
- [Backtesting Reference](artifact/backtesting-reference.md) <br>
- [Trading Reference](artifact/trading-reference.md) <br>
- [FinLabDataFrame Reference](artifact/dataframe-reference.md) <br>
- [Factor Analysis Reference](artifact/factor-analysis-reference.md) <br>
- [Best Practices](artifact/best-practices.md) <br>
- [uv Documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include FinLab backtest metrics, strategy code, setup commands, and order-preview guidance when requested.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
