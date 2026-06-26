## Description: <br>
Provides Chinese mainland A-share market quotes, individual stock technical and fundamental analysis, market sentiment, sector trends, trading strategy suggestions, and price-alert guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to ask an agent for Chinese mainland A-share stock quotes, market analysis, sector trends, trading strategy suggestions, and price-alert guidance. Outputs should be treated as informational market data and analysis support, not personalized investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market-data and trading-strategy outputs could be mistaken for personalized financial advice. <br>
Mitigation: Use outputs as informational analysis support only, require risk notices on price or strategy suggestions, and make final investment decisions outside the agent. <br>
Risk: The skill may use a Wendian API key for market-data requests. <br>
Mitigation: Scope the API key to this service, avoid sharing it beyond the agent environment, and install the skill only when those external market-data requests are intended. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with structured tables, short analysis sections, and inline shell commands when data-fetching commands are shown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stock analysis outputs should include data source, retrieval time, and risk notices when giving price or strategy suggestions.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
