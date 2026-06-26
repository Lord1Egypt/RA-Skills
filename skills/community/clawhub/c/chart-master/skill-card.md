## Description: <br>
Generate precise financial charts for stocks, indices, and crypto using Python-based market data and charting tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericw12](https://clawhub.ai/user/ericw12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate visual financial price-history and technical-analysis charts for requested tickers, date ranges, intervals, chart styles, and moving averages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install Python charting and market-data packages at runtime. <br>
Mitigation: Run it in an environment where runtime package installation is permitted, or preinstall the required packages from trusted package sources. <br>
Risk: The skill contacts yfinance to retrieve public market data. <br>
Mitigation: Use it only where outbound access to public market-data services is acceptable, and treat retrieved data as external data rather than authoritative financial advice. <br>
Risk: The skill creates PNG files in the working directory or requested output directory. <br>
Mitigation: Choose an appropriate output directory and review generated file paths before sharing or retaining outputs. <br>


## Reference(s): <br>
- [Chart Master on ClawHub](https://clawhub.ai/ericw12/chart-master) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated PNG chart files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script prints the generated file path and a MEDIA line with the absolute PNG path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
