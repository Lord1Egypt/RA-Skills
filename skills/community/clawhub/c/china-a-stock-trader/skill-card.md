## Description: <br>
China A Stock Trader helps an agent analyze China A-share equities with real-time market data, technical indicators, fundamental screening, market-sentiment checks, risk flags, and trading-style guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxie48892-jpg](https://clawhub.ai/user/dxie48892-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for A-share stock analysis, screening, market heat, dragon-tiger list data, and risk-aware buy, hold, or sell guidance. Outputs are informational and should be independently verified before any investment decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts third-party finance data providers and may receive unavailable, delayed, or inaccurate market data. <br>
Mitigation: Verify prices, fundamentals, and financial reports against independent sources before relying on the analysis. <br>
Risk: The skill produces speculative trading-style guidance that may be mistaken for personalized financial advice. <br>
Mitigation: Treat outputs as informational, retain the risk disclaimer in generated reports, and make investment decisions outside the agent workflow. <br>
Risk: Users may disclose brokerage credentials, private portfolio details, or account access even though the skill does not need them. <br>
Mitigation: Do not provide brokerage credentials, private portfolio details, account access, or other sensitive financial information to the skill. <br>


## Reference(s): <br>
- [A-share Stock Code Reference](references/china-stocks.md) <br>
- [ClawHub skill page](https://clawhub.ai/dxie48892-jpg/china-a-stock-trader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown-style analysis with Python dictionary-style data and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public market data from third-party finance providers; does not execute trades or require brokerage credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and artifact metadata, released 2026-03-21) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
