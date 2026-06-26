## Description: <br>
Gangtise 数据库 retrieves structured financial data from the Gangtise Open API, including daily market quotes, financial statements, business composition, shareholder data, valuation metrics, and earnings forecasts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gangtisegts](https://clawhub.ai/user/gangtisegts) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Financial analysts, researchers, and agents use this skill to fetch table-ready securities, valuation, shareholder, forecast, and financial statement data for downstream analysis or charting. It is intended for users who already have Gangtise credentials and complete security codes such as 600519.SH. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shareholder queries can send the authorization token to a URL selected through GANGTISE_DOMAIN. <br>
Mitigation: Before running shareholder queries, leave GANGTISE_DOMAIN unset or set it only to the legitimate Gangtise HTTPS service. <br>
Risk: The skill requires sensitive Gangtise access credentials. <br>
Mitigation: Install only when the publisher is trusted, provide credentials through controlled environment variables or the documented local authorization file, and do not commit credential files. <br>
Risk: Financial research outputs may be saved under workspace/gangtise. <br>
Mitigation: Review and delete generated files when they contain sensitive research, business, or portfolio data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gangtisegts/gangtise-data) <br>
- [Earnings Forecast API](https://open.gangtise.com/application/open-fundamental/earning_forecast) <br>
- [Valuation usage reference](references/valuation.md) <br>
- [Quote usage reference](references/quote.md) <br>
- [Financial statements usage reference](references/financial.md) <br>
- [Main business usage reference](references/main_business.md) <br>
- [Shareholder usage reference](references/shareholder.md) <br>
- [Earnings forecast usage reference](references/earning_forecast.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and CSV file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated CSV files are written under workspace/gangtise by data category.] <br>

## Skill Version(s): <br>
1.4.3 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
