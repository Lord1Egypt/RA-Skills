## Description: <br>
Perform comprehensive technical analysis using 12+ indicators including RSI, MACD, Bollinger Bands, support/resistance, and chart patterns via the Finskills API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[finskills](https://clawhub.ai/user/finskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request technical analysis for US-listed stocks, indexes, or ETFs. It fetches Finskills market data, computes indicators, maps support and resistance, detects patterns, and returns a structured trade setup for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Finskills API key and sends requested ticker symbols to Finskills for market data. <br>
Mitigation: Install only when the user accepts that credential and data-sharing requirement, and provide the key through the documented FINSKILLS_API_KEY environment variable. <br>
Risk: Generated entries, stops, targets, and recommended actions may be mistaken for personalized financial advice or an instruction to trade. <br>
Mitigation: Treat the output as educational technical analysis and review it independently before making any investment decision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/finskills/finskills-technical-analyst) <br>
- [Finskills technical-analyst homepage](https://github.com/finskills/technical-analyst) <br>
- [Finskills API](https://finskills.net) <br>
- [Publisher profile](https://clawhub.ai/user/finskills) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Markdown, Guidance] <br>
**Output Format:** [Markdown technical-analysis report with indicator tables, support and resistance levels, trade setup fields, and explanatory prose] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FINSKILLS_API_KEY and sends requested ticker symbols to the Finskills API; outputs are educational technical analysis, not personalized financial advice or trading authority.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
