## Description: <br>
Provides unified access to multi-source financial market data for stocks, futures, ETFs, real-time quotes, sectors, financials, and macroeconomic indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bjdenglun](https://clawhub.ai/user/bjdenglun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to add Python-based access to A-share, Hong Kong, U.S. equity, futures, ETF, sector, financial statement, fund-flow, and macroeconomic market data. It is suited for agents that need implementation guidance, helper functions, or example commands for market-data retrieval workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is flagged suspicious because it ships with and uses a concrete third-party API key. <br>
Mitigation: Remove or rotate the bundled Eastmoney key before use and configure your own key locally, preferably through an environment variable or secret manager. <br>
Risk: Live market-data requests go to external financial data providers. <br>
Mitigation: Install and run the skill only where external market-data queries are allowed, and review provider terms and data-handling requirements before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bjdenglun/financial-market-data) <br>
- [Eastmoney MX API documentation](https://openapi.eastmoney.com/mx/v1/api-docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request examples, dependency installation commands, and local configuration guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
