## Description: <br>
Chart Library helps agents search historically similar stock chart patterns, compute forward-return analogs, and summarize results for stock-chart research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grahammccain](https://clawhub.ai/user/grahammccain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market-research agents use this skill to query Chart Library for similar historical stock chart patterns, forward-return distributions, and plain-English summaries. It is intended for research support, not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker and date queries, and any configured Chart Library API key, are sent to chartlibrary.io. <br>
Mitigation: Avoid sharing private portfolio, account, or credential details in prompts or configuration. <br>
Risk: Generated market summaries may be mistaken for investment advice. <br>
Mitigation: Frame outputs as historical research, verify important findings independently, and do not present results as predictions or financial advice. <br>


## Reference(s): <br>
- [Chart Library homepage](https://chartlibrary.io) <br>
- [Chart Library API documentation](https://chartlibrary.io/developers) <br>
- [Chart Library OpenAPI specification](https://chartlibrary.io/api/openapi.json) <br>
- [Chart Library AI plugin manifest](https://chartlibrary.io/.well-known/ai-plugin.json) <br>
- [ClawHub release page](https://clawhub.ai/grahammccain/chart-library) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown or plain-text summaries with structured API response data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include match counts, forward-return distributions, median returns, ranges, similarity notes, and AI-generated summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
