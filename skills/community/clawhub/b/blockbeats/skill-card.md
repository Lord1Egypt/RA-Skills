## Description: <br>
BlockBeats Skill covers over 1,500 information sources, including AI-driven insights, Hyperliquid on-chain data, and Polymarket market analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blockbeatsofficial](https://clawhub.ai/user/blockbeatsofficial) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query BlockBeats crypto news, article search, market summaries, on-chain signals, derivatives data, and macro market indicators through the BlockBeats Pro API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad news or market prompts could route generic requests to BlockBeats unintentionally. <br>
Mitigation: Use explicit wording such as 'BlockBeats crypto news' or 'search BlockBeats for...' when invoking the skill. <br>
Risk: The skill makes outbound BlockBeats API requests using a BlockBeats API key. <br>
Mitigation: Install only if you trust BlockBeats, keep the API key scoped and protected, and monitor API usage or quota. <br>


## Reference(s): <br>
- [BlockBeats Skill on ClawHub](https://clawhub.ai/blockbeatsofficial/blockbeats) <br>
- [BlockBeats Pro API Base URL](https://api-pro.theblockbeats.info) <br>
- [BlockBeats API Key Application](https://www.theblockbeats.info/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with optional curl commands and API response interpretation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and BLOCKBEATS_API_KEY; formats API responses into crypto news, search results, market data, and market-analysis guidance.] <br>

## Skill Version(s): <br>
1.0.4 (source: release evidence; artifact frontmatter reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
