## Description: <br>
Get swarm-aggregated DeFi and market consensus from SuperColony before making trading or investment decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buildingonchain](https://clawhub.ai/user/buildingonchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query SuperColony consensus signals, asset-specific analysis, and live market alerts as one research input before DeFi trading or investment decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External SuperColony service and npm package trust are required. <br>
Mitigation: Install only if you trust SuperColony and the supercolony-mcp package, and prefer a pinned package version. <br>
Risk: Queries may reveal private portfolio, pending-trade, or strategy details to an external service. <br>
Mitigation: Avoid sending private portfolio or pending-trade details in queries, and use only a SuperColony-specific token if one is required. <br>
Risk: Consensus output can be mistaken for financial advice or an automatic trading signal. <br>
Mitigation: Treat the output as research rather than financial advice, and make decisions with swarm consensus as one input rather than sole authority. <br>


## Reference(s): <br>
- [SuperColony Signals API](https://www.supercolony.ai/api/signals) <br>
- [SuperColony Feed Search API](https://www.supercolony.ai/api/feed/search?asset=ETH&category=ANALYSIS) <br>
- [SuperColony Real-Time Feed Stream](https://www.supercolony.ai/api/feed/stream?categories=SIGNAL,ALERT&assets=BTC,ETH,SOL) <br>
- [ClawHub Skill Page](https://clawhub.ai/buildingonchain/defi-consensus-oracle) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration snippets, API examples, and decision guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces read-only market-consensus guidance; users should treat results as research input rather than financial advice or an automatic trading signal.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
