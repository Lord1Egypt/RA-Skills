## Description: <br>
Technical analysis and chart pattern recognition for equities, options, and crypto markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CollierKing](https://clawhub.ai/user/CollierKing) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and trading workflows use this skill to ask an agent for technical chart analysis, pattern recognition, support and resistance levels, trend classification, and multi-timeframe market setup summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required ChartClass API key could be exposed if pasted into prompts, shared files, or logs. <br>
Mitigation: Provide CHARTCLASS_API_KEY through the documented environment variable, keep it secret, and avoid including it in agent-visible text. <br>
Risk: Financial chart analysis may be incorrect, incomplete, or misread as guaranteed investment advice. <br>
Mitigation: Treat outputs as analysis support, verify important conclusions against trusted market data, and apply appropriate human review before trading or investment decisions. <br>
Risk: Authenticated API usage may consume account quota or incur unexpected usage. <br>
Mitigation: Monitor ChartClass account or quota usage when enabling the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CollierKing/chartclass) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown or plain text analysis with configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CHARTCLASS_API_KEY for market data access; CHARTCLASS_DEFAULT_TIMEFRAME may set the default chart timeframe.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
