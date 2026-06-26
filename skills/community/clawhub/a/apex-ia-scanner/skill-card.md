## Description: <br>
Professional scanner for Binance Futures that reports SMA 8/21 crossover signals and multi-timeframe trading setups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcusfranca12](https://clawhub.ai/user/marcusfranca12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to scan Binance Futures markets for SMA 8/21 crossover signals, scores, and setup summaries. Outputs should be reviewed as trading analysis, not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence reports that the package is advertised as a Binance Futures scanner but includes code that can automatically place leveraged futures trades using embedded Binance credentials. <br>
Mitigation: Do not run it with real exchange permissions unless trading files are removed or audited, embedded keys are revoked and replaced with least-privilege user-managed credentials, auto-trading is disabled by default, and every account-changing action requires clear user approval. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/marcusfranca12/apex-ia-scanner) <br>
- [Binance Futures Kline API](https://fapi.binance.com/fapi/v1/klines) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with ranked trading-signal summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns symbols, direction, timeframe, score, RSI, volume ratio, targets, stop, risk-reward, and confluence when available.] <br>

## Skill Version(s): <br>
2.4.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
