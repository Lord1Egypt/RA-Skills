## Description: <br>
Queries financial market data for stocks, ETFs, cryptocurrencies, and similar instruments when the user asks about prices, quotes, ticker symbols, or recent history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iyuanfang](https://clawhub.ai/user/iyuanfang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to look up recent market quote data, date ranges, and composite score fields for supported securities through the Financial Agent API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends requested symbols and API keys to api.financialagent.cc for quote lookup. <br>
Mitigation: Use the API only when that data sharing is acceptable, and prefer a dedicated low-privilege API key. <br>
Risk: The documented key setup edits the main OpenClaw configuration file and may overwrite existing custom settings if applied without review. <br>
Mitigation: Back up ~/.openclaw/openclaw.json and confirm the jq update preserves existing custom configuration before saving a key. <br>


## Reference(s): <br>
- [Financial Agent API](https://api.financialagent.cc) <br>
- [ClawHub skill page](https://clawhub.ai/iyuanfang/financial-ai-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API response interpretation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include quote lookup commands, API key configuration steps, and explanations of returned composite score and level fields.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
