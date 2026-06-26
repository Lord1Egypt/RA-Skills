## Description: <br>
A股智投大师 is an A-share investment research assistant for market quotes, fundamentals, stock screening, watchlist management, monitoring alerts, and news analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucasxing1](https://clawhub.ai/user/lucasxing1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to analyze Chinese A-share equities, screen stocks, review watchlists, and set monitoring alerts using Eastmoney Miaoxiang data. Outputs are informational and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auto-installed companion skills and external data access can broaden what the agent is able to call. <br>
Mitigation: Review the companion skills before installation and use only the intended Eastmoney API key. <br>
Risk: Watchlist changes or monitoring alerts can affect user-maintained investment workflows. <br>
Mitigation: Require the agent to confirm the exact stock, action, and alert rule before modifying watchlists or creating monitoring alerts. <br>
Risk: Market analysis can be incomplete, delayed, or misleading if treated as investment advice. <br>
Mitigation: Present outputs as informational, include risk context, and ask users to verify against authoritative market data before making decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lucasxing1/a-stock-analyst) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown and structured analysis summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Eastmoney Miaoxiang API key via companion skills; analysis should include risk context and avoid being presented as financial advice.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
