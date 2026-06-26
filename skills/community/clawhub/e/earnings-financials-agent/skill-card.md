## Description: <br>
An autonomous agent for monitoring corporate earnings and analyzing financial statements using yfinance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[assix](https://clawhub.ai/user/assix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and financial analysts use this local Python skill to retrieve public earnings calendars and recent financial statement metrics for ticker-based financial analysis. The output should support analysis workflows and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill retrieves public stock data through yfinance, so results can be delayed, incomplete, or different from official filings. <br>
Mitigation: Use the output as supporting data and verify material decisions against official company filings or trusted market data sources. <br>
Risk: Installing an unpinned Python dependency can reduce reproducibility or introduce unexpected dependency changes. <br>
Mitigation: Install in a virtual environment and pin yfinance to a reviewed version where reproducible behavior is required. <br>
Risk: Financial summaries may be mistaken for investment advice. <br>
Mitigation: Present outputs as data analysis only and require human review before acting on investment, trading, or compliance decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/assix/earnings-financials-agent) <br>
- [Publisher profile](https://clawhub.ai/user/assix) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown instructions with local Python command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, pip, and the yfinance Python package.] <br>

## Skill Version(s): <br>
1.0.3 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
