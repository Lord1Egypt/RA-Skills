## Description: <br>
AkShare Stock Data Pro helps agents retrieve A-share, Hong Kong, and U.S. stock market data through AkShare, including quotes, history, financials, shareholder data, capital flows, sector data, IPOs, block trades, valuation metrics, and ESG ratings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhengr](https://clawhub.ai/user/zhengr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to fetch market datasets for analysis, reporting, and stock research workflows. Outputs should be treated as market data, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts external market-data sources and may return large CSV datasets. <br>
Mitigation: Run only the needed AkShare command or API call, scope requests to relevant symbols and dates, and review large outputs before relying on them. <br>
Risk: Market data returned by the skill may be delayed or incomplete and should not be treated as investment advice. <br>
Mitigation: Validate important results against authoritative sources and apply independent financial review before making decisions. <br>
Risk: Users could accidentally provide browser cookies, account sessions, or API tokens while asking for data access. <br>
Mitigation: Do not paste secrets into chat or command arguments; use the documented public-data workflows and redact sensitive values. <br>


## Reference(s): <br>
- [AkShare Stock Data API Reference](references/api_reference.md) <br>
- [ClawHub release page](https://clawhub.ai/zhengr/akshare-stock-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; command output is CSV or JSON market data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May contact external market-data sources through AkShare and may return large datasets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
