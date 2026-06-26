## Description: <br>
A quantitative trading workspace for A-share and futures workflows that supports multi-factor stock screening, A-share backtesting, QMT and Wenhua execution, and risk monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonstang](https://clawhub.ai/user/simonstang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate stock-picking outputs, backtest A-share strategies, configure broker execution adapters, and monitor trading risk. It is not a substitute for investment advice, audited trading systems, or broker-side controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live broker execution paths can place real trades or close positions when configured for live QMT or Wenhua access. <br>
Mitigation: Use paper mode unless the executors have been audited, require explicit confirmation for every live order and close_all action, and tightly scope broker credentials. <br>
Risk: Default stock-picking, risk-monitoring, and backtest paths include simulated or randomly generated data in artifact behavior. <br>
Mitigation: Replace demo data with validated market data, label outputs as non-investment-grade until verified, and review assumptions before relying on reports. <br>
Risk: Telegram notification settings can expose tokens, chat identifiers, or sensitive trading information. <br>
Mitigation: Store notification credentials securely, disable notifications when not needed, and avoid sending account or order details to broad channels. <br>
Risk: Financial outputs may be mistaken for investment advice or automated trading approval. <br>
Mitigation: Require qualified human review, broker-side limits, and independent risk controls before any production trading use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simonstang/bowlong-quant-aio) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/simonstang) <br>
- [README](artifact/README.md) <br>
- [Optimization V2.1 notes](artifact/docs/OPTIMIZATION_V2.1.md) <br>
- [Sample momentum backtest report](artifact/output/backtest_reports/backtest_report_momentum_20260327_193303.md) <br>
- [Project homepage](https://learn2study.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, CSV stock-pick files, Markdown backtest and risk reports, Python code, shell commands, and YAML configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce broker execution commands and financial analysis outputs; outputs require human review before trading use.] <br>

## Skill Version(s): <br>
2.1.3 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
