## Description: <br>
Provides no-key cryptocurrency and stock market data tools for real-time prices, company profiles, historical charts, and global analytics using Node.js with zero external dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Liam8](https://clawhub.ai/user/Liam8) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to retrieve cryptocurrency and stock market data, including prices, search results, company profiles, historical charts, global market metrics, and public-company crypto holdings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested symbols, coin IDs, currencies, and search terms are sent to api.igent.net. <br>
Mitigation: Install and use the skill only when that external API disclosure is acceptable for the intended workload. <br>
Risk: The skill caches a provider session token in scripts/.token. <br>
Mitigation: Keep the skill directory private and delete scripts/.token when clearing the cached provider session. <br>
Risk: API_BASE_URL can redirect requests to a replacement service. <br>
Mitigation: Avoid setting API_BASE_URL unless the replacement market-data service is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Liam8/crypto-market-data) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON from Node.js command-line scripts, with Markdown usage guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on live responses from the configured market-data API service.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
