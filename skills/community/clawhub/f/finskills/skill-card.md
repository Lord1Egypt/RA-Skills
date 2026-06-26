## Description: <br>
Finskills provides a real-time financial data API for systematic stock analysis and quantitative investment research across quotes, historical OHLCV, fundamentals, earnings, analyst recommendations, options, institutional holders, macro indicators, commodities, SEC filings, financial news, and crypto. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[finskills](https://clawhub.ai/user/finskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to retrieve Finskills market data and produce factual stock, macro, options, commodity, crypto, SEC filing, and financial-news analysis for systematic investment research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Finskills API keys are required for authenticated requests. <br>
Mitigation: Provide the key through an environment variable or approved secret mechanism, avoid pasting it into ordinary chat, and rotate it if exposed. <br>
Risk: Market-data outputs can be mistaken for financial advice or trade instructions. <br>
Mitigation: Use outputs for planning and education, present data factually with freshness and units, and require human review before trading. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/finskills/finskills) <br>
- [Finskills homepage](https://finskills.net) <br>
- [Finskills API documentation](https://finskills.net/documentation) <br>
- [Finskills skill page](https://finskills.net/skill) <br>
- [Anthropic Skills specification](https://github.com/anthropics/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with market-data summaries, endpoint guidance, and optional shell command blocks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include units, data freshness, and factual framing; they should not be treated as financial advice.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
