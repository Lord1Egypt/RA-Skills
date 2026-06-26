## Description: <br>
전문 투자 분석가 AI로, 한국 주식 종목의 재무제표, 뉴스, 차트를 분석하여 Investment Attractiveness Score (0-100)와 BUY/HOLD/AVOID 추천을 제공합니다. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Saebyeok-Im](https://clawhub.ai/user/Saebyeok-Im) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and analysts use this skill to evaluate Korean KRX-listed equities with a conservative framework that prioritizes financial fundamentals, then news outlook, then chart timing. It produces a structured score and BUY, BUY_LEAN, HOLD, or AVOID verdict for supported Korean stock tickers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional scripts scrape Naver Finance and may depend on live page structure, browser state, local command execution, or hardcoded paths. <br>
Mitigation: Review scripts before execution, run them in a clean browser profile, adjust local paths, and verify scraped data against source pages before relying on reports. <br>
Risk: Generated equity scores can be incomplete or misleading if market data, news summaries, or chart descriptions are missing, stale, or incorrectly extracted. <br>
Mitigation: Treat outputs as analysis support rather than financial advice, confirm source data manually, and preserve the framework's financial-priority scoring rules. <br>


## Reference(s): <br>
- [Equity Analysis Framework](references/framework.md) <br>
- [Naver Finance ticker page](https://finance.naver.com/item/main.naver?code={ticker}) <br>
- [ClawHub skill page](https://clawhub.ai/Saebyeok-Im/equity-analyst) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, guidance] <br>
**Output Format:** [Structured Markdown report with numeric scores, verdict, and reasoning summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focused on Korean stocks; optional scripts can create report files from Naver Finance data.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
