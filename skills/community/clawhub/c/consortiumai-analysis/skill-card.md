## Description: <br>
Gets the latest AI-generated crypto trading analysis (BUY / SELL / WAIT) for spot trading pairs from the Consortium AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WebCraft3r](https://clawhub.ai/user/WebCraft3r) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to fetch the latest Consortium AI trading analysis for crypto spot pairs, either overall or filtered by a base token. It supports read-only market-signal retrieval and summarization rather than automated trading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading signals may be mistaken for guaranteed outcomes or financial advice. <br>
Mitigation: Treat BUY, SELL, and WAIT outputs as informational analysis only, and require user judgment before any trading decision. <br>
Risk: Using the skill sends requested token symbols to api.consortiumai.org and requires an API key. <br>
Mitigation: Use a dedicated TRADING_ANALYSIS_API_KEY stored in the environment, and only query token symbols the user intends to share with Consortium AI. <br>
Risk: The API can return authentication errors, missing-analysis responses, or server failures. <br>
Mitigation: Surface the returned error JSON and avoid fabricating a trading decision when the API does not provide one. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/WebCraft3r/consortiumai-analysis) <br>
- [Consortium AI website](https://consortiumai.org/) <br>
- [Trading Analysis API endpoint](https://api.consortiumai.org/api/trading-analysis) <br>
- [Consortium AI on X](https://x.com/Consortium_AI) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Analysis, Guidance, Shell commands] <br>
**Output Format:** [JSON API response that an agent can summarize as text or markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRADING_ANALYSIS_API_KEY; accepts an optional base token symbol; returns at most the latest matching trading decision.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
