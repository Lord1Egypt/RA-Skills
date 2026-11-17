## Description:

A Stock Screener helps agents screen China A-share stocks with a five-step workflow covering quantitative filters, fundamentals, capital flows, industry themes, and risk checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nodermachine](https://clawhub.ai/user/nodermachine)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run or request a structured A-share stock screen, generate a stock-pool report, export an Excel result, and tune screening conditions. Results are preliminary research and should be confirmed against official disclosures and current market data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated stock lists may be incomplete or misleading because several screening checks are simplified.

Mitigation: Treat outputs as preliminary research and verify results against official disclosures and current market data before making financial decisions.

Risk: The script depends on external Python packages and market data sources.

Mitigation: Install dependencies only in a virtual environment and review dependency sources before running the script.

## Reference(s):

- [A-share industry track guide](references/industry_guide.md)
- [Eastmoney](https://www.eastmoney.com/)
- [iWencai](https://www.iwencai.com/)
- [CNINFO](http://www.cninfo.com.cn/)
- [Tushare](https://tushare.pro/)
- [Baostock](http://baostock.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance, terminal output, and optional Excel files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write an .xlsx stock-pool export when the screening script is run with an output path.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
