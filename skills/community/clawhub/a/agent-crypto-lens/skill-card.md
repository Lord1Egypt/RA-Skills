## Description: <br>
Analyzes cryptocurrency token market trends and sentiment using CoinGecko market data, web news, and an LLM-generated report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinu4you](https://clawhub.ai/user/jinu4you) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and crypto analysts use this agent to request token-level market and sentiment summaries for a named cryptocurrency, including market data, recent news context, scores, and a short report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Relevant token names, news snippets, market data, prompts, and derived sentiment text may be sent to Google Gemini during analysis. <br>
Mitigation: Do not include private trading strategies, regulated data, secrets, or proprietary research unless that disclosure is acceptable under your policies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jinu4you/agent-crypto-lens) <br>
- [Publisher profile](https://clawhub.ai/user/jinu4you) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [JSON object containing market data, sentiment scores, a Markdown report, and success or error metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a token input and optional analysis_type of market, sentiment, or full.] <br>

## Skill Version(s): <br>
1.0.1 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
