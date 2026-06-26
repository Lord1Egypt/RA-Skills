## Description: <br>
为股票代码生成结合缠论技术面、基本面、财报和估值分析的中文投研报告，并输出 Markdown 和 PDF 报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ywwzzsgit](https://clawhub.ai/user/ywwzzsgit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill after providing an A-share, Hong Kong, or U.S. stock code to obtain a structured research report covering technical analysis, fundamentals, valuation, risk, and action guidance. The generated ratings, price targets, stop-losses, and position sizes are research assistance only and should be independently verified before trading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill produces buy/sell ratings, targets, stop-losses, and position sizing that could be mistaken for definitive investment advice. <br>
Mitigation: Treat outputs as research assistance only and independently verify data, assumptions, and conclusions before making trades. <br>
Risk: The skill calls external finance and search services and depends on a Tushare token through its data dependency. <br>
Mitigation: Configure credentials through environment variables, avoid embedding secrets in prompts or reports, and review which external services are contacted. <br>
Risk: The skill may install reportlab at runtime to generate PDF reports. <br>
Mitigation: Run it in an environment where dependency installation is expected, or preinstall and review reportlab before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ywwzzsgit/chanlun-stock-analysis) <br>
- [Tushare data service](https://tushare.pro) <br>
- [缠论（缠中说禅）技术分析参考手册](references/chan-theory.md) <br>
- [基本面与财报分析参考手册](references/financial-analysis.md) <br>
- [估值分析参考手册](references/valuation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Chinese Markdown research report with optional generated PDF and supporting Python commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a Markdown report, a PDF report, and a temporary Python script for PDF rendering; requires configured market data access through the finance-data-retrieval skill and Tushare token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
