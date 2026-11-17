## Description:

Chinese-language stock analysis assistant for A-share, Hong Kong, and U.S. equities that fetches public market data, interprets technical and fundamental indicators, and generates structured research reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryanlee-gemini](https://clawhub.ai/user/ryanlee-gemini)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to request Chinese-language stock analysis by ticker or company name and receive a report covering market data, technical indicators, valuation metrics, ratings, target prices, and risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may fetch public market data from third-party finance sites that can be delayed, incomplete, or inaccessible.

Mitigation: Require reports to disclose data sources, analysis time, and missing data, and to fall back to qualitative analysis only when data is limited.

Risk: The skill produces ratings, target prices, and operation suggestions that could be mistaken for personalized financial advice.

Mitigation: Keep the artifact's disclaimer in generated reports and treat outputs as informational analysis rather than investment recommendations.

## Reference(s):

- [Stock Analysis Report Template](artifact/references/report-template.md)
- [ClawHub Skill Page](https://clawhub.ai/ryanlee-gemini/skills/cn-stock-analyst)
- [Eastmoney Quote Example](https://quote.eastmoney.com/SH600519.html)
- [Eastmoney K-Line API Example](https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=1.600519&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58&klt=101&fqt=1&beg=0&end=20500101&lmt=120)
- [Yahoo Finance Chart API Example](https://query1.finance.yahoo.com/v8/finance/chart/AAPL?interval=1d&range=3mo)
- [Sina Finance Quote Example](https://finance.sina.com.cn/realstock/company/sh600519/nc.shtml)
- [Tencent Finance Quote Example](https://gu.qq.com/sh600519)
- [Xueqiu Quote Example](https://xueqiu.com/S/SH600519)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown stock analysis report with tables, ratings, target prices, operating suggestions, and risk notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include delayed or incomplete public market data; reports must state missing data and are not personalized financial advice.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
