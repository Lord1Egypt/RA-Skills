## Description: <br>
Get real-time stock, ETF, and crypto prices, compare tickers, and check market cap and volume using Yahoo Finance without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[josephflu](https://clawhub.ai/user/josephflu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request current stock, ETF, and cryptocurrency quotes, compare multiple tickers, and view market status and basic market metrics from Yahoo Finance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested ticker symbols are sent to Yahoo Finance. <br>
Mitigation: Use the skill only when sharing requested stock, ETF, or crypto ticker symbols with Yahoo Finance is acceptable. <br>
Risk: Python dependencies are declared for runtime installation. <br>
Mitigation: Pin and review dependencies in environments with stricter supply-chain controls. <br>


## Reference(s): <br>
- [Common Tickers Quick Reference](references/common-tickers.md) <br>
- [Project Homepage](https://github.com/josephflu/clawhub-skills) <br>
- [ClawHub Skill Page](https://clawhub.ai/josephflu/eagerbots-stock-quote) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with command examples and terminal-formatted quote tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs market data for user-requested ticker symbols; requested symbols are sent to Yahoo Finance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
