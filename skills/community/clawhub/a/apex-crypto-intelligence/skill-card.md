## Description: <br>
AI-powered multi-exchange crypto market analysis, arbitrage detection, and hedge fund-quality trading reports using live data from major exchanges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[contrario](https://clawhub.ai/user/contrario) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request cryptocurrency market scans, cross-exchange arbitrage analysis, and AI-generated trading reports from live exchange data. It is informational analysis only and does not execute trades or transfer funds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles exchange API secrets and may contact CoinGecko and exchange APIs when client.py is run. <br>
Mitigation: Use read-only exchange keys only, with trading and withdrawal permissions disabled, and review network behavior before installing or running the skill. <br>
Risk: The security summary says the verification mode may present live third-party network calls as if nothing is transmitted. <br>
Mitigation: Do not treat the verification script as an offline audit until that wording and behavior are fixed. <br>
Risk: The external analysis service receives market data and query text for AI analysis. <br>
Mitigation: Avoid including personal data, wallet addresses, credentials, or sensitive trading strategy details in queries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/contrario/apex-crypto-intelligence) <br>
- [Publisher profile](https://clawhub.ai/user/contrario) <br>
- [Project homepage and privacy policy](https://masterswarm.net) <br>
- [External analysis endpoint](https://api.neurodoc.app/aetherlang/execute) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Text or Markdown analysis with optional report-oriented output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include market summaries, arbitrage observations, risk commentary, and trading blueprint content; does not place trades.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
