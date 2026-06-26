## Description: <br>
Stock momentum scanner and portfolio intelligence for ticker lookup, market signals, portfolio alerts, sector trends, win/loss proof data, and risk assessment through natural conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adamandjarvis](https://clawhub.ai/user/adamandjarvis) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to query Banana Farmer market intelligence from an agent, including ticker momentum, top signals, portfolio briefs, watchlists, sector comparisons, historical signal performance, and market health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker requests and portfolio symbols may be sent to Banana Farmer as an external market-data provider. <br>
Mitigation: Keep portfolio files minimal, avoid unnecessary sensitive account details, and use the skill only when comfortable sending requested symbols to bananafarmer.app. <br>
Risk: BF_API_KEY is required for API access and could expose the user's Banana Farmer account if mishandled. <br>
Mitigation: Store BF_API_KEY in the environment or agent secret configuration, keep it private, and do not paste it into prompts or shared files. <br>
Risk: Scores, alerts, historical win rates, and return figures can be mistaken for investment advice or guaranteed performance. <br>
Mitigation: Treat all outputs as informational research, check data freshness, and consult qualified financial advice before making investment decisions. <br>
Risk: Market data can be delayed or stale, especially for stock data and during service outages. <br>
Mitigation: Run the market health check before acting on signals and note stale data in any analysis. <br>


## Reference(s): <br>
- [Banana Farmer](https://bananafarmer.app) <br>
- [Banana Farmer Developers](https://bananafarmer.app/developers) <br>
- [Tiingo Market Data](https://tiingo.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown-style terminal output, command examples, and optional JSON from selected scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and BF_API_KEY; scripts use outbound HTTPS calls to bananafarmer.app and some endpoints may depend on API tier.] <br>

## Skill Version(s): <br>
1.9.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
