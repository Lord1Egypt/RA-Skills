## Description: <br>
Calculate asset allocation weights for a portfolio of ETFs based on Risk Parity (All Weather) principles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wzwangyc](https://clawhub.ai/user/wzwangyc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to calculate ETF portfolio weights, allocation amounts, and annualized return and volatility estimates for a risk-parity All Weather strategy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill produces portfolio allocations and forecasts that could be mistaken for personalized financial advice. <br>
Mitigation: Present allocations and forecasts as informational analysis only and require independent review before any trading decision. <br>
Risk: The skill depends on external market-data services and Python packages whose results or behavior can change over time. <br>
Mitigation: Run it in an isolated Python environment, review or pin dependencies, and verify market data before relying on outputs. <br>
Risk: Report export can create CSV or PDF files in the execution environment. <br>
Mitigation: Run in a workspace where generated report files are expected and review outputs before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wzwangyc/all-weather-strategy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown or tabular text with optional CSV and PDF report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ETF market data from AkShare and yfinance when calculations are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
