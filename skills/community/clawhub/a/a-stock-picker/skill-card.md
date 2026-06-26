## Description: <br>
A股三层选股模型 uses a three-stage funnel of quantitative screening, qualitative analysis, and timing guidance to help an agent evaluate China A-share stock candidates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danpian1](https://clawhub.ai/user/danpian1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, analysts, and agents use this skill to scan China A-share markets, review candidates against quantitative and qualitative criteria, and draft informational watchlists or trading-plan suggestions with risk controls. <br>

### Deployment Geography for Use: <br>
Global; market coverage is China A-shares. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce specific trading-plan suggestions that may be mistaken for personalized or regulated financial advice. <br>
Mitigation: Treat outputs as informational drafts, verify assumptions independently, and have a qualified reviewer decide whether any action is appropriate. <br>
Risk: Market data and screener results can be stale, incomplete, unavailable, or affected by endpoint changes. <br>
Mitigation: Check data freshness and compare results against authoritative market and financial data before relying on the analysis. <br>
Risk: The Python screener reaches external market-data endpoints during execution. <br>
Mitigation: Run it only in environments where outbound network access to the listed data providers is expected and acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danpian1/a-stock-picker) <br>
- [SKILL.md](SKILL.md) <br>
- [Qualitative analysis framework](references/analysis-framework.md) <br>
- [Quantitative screening rules](references/screening-rules.md) <br>
- [Sina Finance market data endpoint](https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php) <br>
- [Tencent K-line data endpoint](https://web.ifzq.gtimg.cn/appstock/app/fqkline/get) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown sections and tables, with optional Python screener execution output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include stock tickers, scores, buy ranges, stop-loss levels, target prices, position suggestions, and risk ratings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
