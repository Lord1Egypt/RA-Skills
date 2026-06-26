## Description: <br>
BlockBeats Skill covers over 1,500 information sources, including AI-driven insights, Hyperliquid on-chain data, and Polymarket market analytics. It also features robust keyword-based search functionality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blockbeatsofficial](https://clawhub.ai/user/blockbeatsofficial) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query the BlockBeats Pro API for crypto news, keyword search, market overviews, capital-flow analysis, macro indicators, derivatives data, on-chain data, and RSS-style updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent uses the user's BlockBeats API key for read-only crypto news, search, and market-data requests. <br>
Mitigation: Install only when comfortable sharing relevant lookup queries with BlockBeats, keep the key scoped to this use, and rotate or revoke it if exposed. <br>
Risk: Broad market or news questions may consume BlockBeats API quota. <br>
Mitigation: Prefer targeted queries and set user expectations before running broad or repeated market-data lookups. <br>
Risk: Market interpretations may be mistaken for financial advice. <br>
Mitigation: Present buy, sell, and sentiment signals as informational context rather than investment recommendations. <br>


## Reference(s): <br>
- [BlockBeats Pro API Base URL](https://api-pro.theblockbeats.info) <br>
- [ClawHub Skill Page](https://clawhub.ai/blockbeatsofficial/blockbeats-skill) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/blockbeatsofficial) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries with inline bash commands and API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and BLOCKBEATS_API_KEY; responses may include crypto news, market indicators, on-chain data, and interpretive summaries.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
