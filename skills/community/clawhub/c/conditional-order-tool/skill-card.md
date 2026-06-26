## Description: <br>
Helps agents identify ETF or stock categories from Chinese market codes, recommend conditional-order strategies, and draft parameterized analysis reports with investment-risk disclaimers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lj22503](https://clawhub.ai/user/lj22503) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to analyze Chinese ETF or stock codes, choose suitable conditional-order patterns, and generate educational parameter suggestions for review before acting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake conditional-order parameters for personalized financial advice. <br>
Mitigation: Present outputs as educational starting points, keep the investment-risk disclaimer visible, and require the user to verify suitability independently before acting. <br>
Risk: Live price or premium data may be unavailable, stale, or blocked by the public data source. <br>
Mitigation: Clearly label fallback/reference parameters and instruct users to manually verify instrument identity, current price, premium, and risk before placing any order. <br>
Risk: The ETF database is finite and may not recognize new or unsupported instruments. <br>
Mitigation: Ask the user to confirm unknown codes and avoid producing confident strategy recommendations when the instrument type is unresolved. <br>
Risk: Users might provide broker credentials or expect the skill to execute trades. <br>
Mitigation: Do not request credentials, do not execute trades, and keep the skill limited to public market-data lookup and written guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lj22503/conditional-order-tool) <br>
- [Publisher profile](https://clawhub.ai/user/lj22503) <br>
- [Strategy matrix](references/strategy-matrix.md) <br>
- [ETF database](references/etf-database.md) <br>
- [Eastmoney quotes](https://quote.eastmoney.com/) <br>
- [Tencent Finance](https://finance.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown analysis reports with structured strategy parameters and optional JSON from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes investment-risk disclaimers and may fall back to reference values when live public price data is unavailable.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
