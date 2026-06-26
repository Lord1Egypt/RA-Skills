## Description: <br>
Provides technical stock analysis using MACD, KDJ, SAR, moving averages, OBV, PVT, Bollinger Bands, CCI, and RSI, with automated breakout, volume, risk, and trading-signal summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[footballqq](https://clawhub.ai/user/footballqq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and investment-analysis agents use this skill to generate technical-analysis reports for supported stock symbols and market-index questions. It is intended for informational market analysis and decision support, not as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill produces market-analysis output that could be mistaken for investment advice. <br>
Mitigation: Treat all output as informational only, retain the included disclaimer, and require users to make independent investment decisions. <br>
Risk: The bundled analyzer runs local Python code and depends on third-party market-data libraries. <br>
Mitigation: Install dependencies only from trusted sources and review the script before execution in managed environments. <br>
Risk: Technical indicators can lag market conditions or reflect incomplete data. <br>
Mitigation: Cross-check generated analysis against current market data, fundamentals, policy context, and other independent sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/footballqq/ai-quant-skill) <br>
- [Publisher profile](https://clawhub.ai/user/footballqq) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Text or Markdown report with technical indicators, risk notes, and signal summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke a local Python script and third-party market-data libraries; results are informational and include a financial-risk disclaimer.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
