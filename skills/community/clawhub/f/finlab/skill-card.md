## Description:

Comprehensive guide for FinLab quantitative trading package. Use when working with trading strategies, backtesting, stock data, FinLabDataFrame, factor analysis, stock selection, or when the user mentions FinLab, trading, quant trading, or stock market analysis. Includes data access, strategy development, backtesting workflows, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[koreal6803](https://clawhub.ai/user/koreal6803)

### License/Terms of Use:


## Use Case:

Developers and quantitative trading practitioners use this skill to build FinLab data workflows, factor screens, backtests, machine-learning experiments, and optional broker order-execution flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading guidance can lead to real broker orders without sufficient confirmation boundaries.

Mitigation: Use preview-only or paper trading unless the exact orders, account, quantities, and prices are explicitly approved.

Risk: Broker integrations require credentials, tokens, account identifiers, and certificate paths.

Mitigation: Keep real broker credentials and API tokens out of chats and notebooks, and use an isolated locked Python environment.

Risk: Experimental backtests may upload strategy reports or produce misleading results if future data leaks into the workflow.

Mitigation: Keep experiments at `upload=False`, review lookahead-bias guidance, and validate strategies before relying on results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/koreal6803/skills/finlab)
- [uv Package Manager Documentation](https://docs.astral.sh/uv/)
- [Data Reference](data-reference.md)
- [Backtesting Reference](backtesting-reference.md)
- [Trading & Order Execution Reference](trading-reference.md)
- [FinlabDataFrame Reference](dataframe-reference.md)
- [Factor Analysis Reference](factor-analysis-reference.md)
- [Factor Examples and Strategy Reference](factor-examples.md)
- [Machine Learning Reference](machine-learning-reference.md)
- [Best Practices and Anti-Patterns](best-practices.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include FinLab backtest code, data-access examples, credential setup guidance, and order-execution guidance.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
