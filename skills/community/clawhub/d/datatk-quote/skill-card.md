## Description: <br>
Real-time stock market data via QuoteNode API. Query quotes, K-lines, tick trades, Level-2 depth, and trading calendars for US/HK/CN markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengxiaozi-liu](https://clawhub.ai/user/fengxiaozi-liu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market-data users use this skill to select QuoteNode REST endpoints, prepare authenticated JSON requests, and inspect quote, K-line, tick, depth, broker, and trading-calendar responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper stores a QuoteNode/dataTrack API key locally and sends the key with request bodies to the configured API endpoint. <br>
Mitigation: Install only if you trust the QuoteNode/dataTrack service, keep env.json out of shared repositories and logs, and review request bodies before running them. <br>
Risk: Requests can consume provider quota or fail when the account lacks endpoint, market, or rate-limit permission. <br>
Mitigation: Use the documented endpoint, market, and parameter references before execution and monitor provider quota and permission errors. <br>


## Reference(s): <br>
- [QuoteNode REST Architecture Summary](references/architecture.md) <br>
- [QuoteNode REST API Guide](references/openapi.md) <br>
- [QuoteNode Enums and Error Codes](references/reference.md) <br>
- [QuoteNode REST Response Field Guide](references/response.md) <br>
- [dataTrack Service Page](https://www.datatk.com/service) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local env.json file for endpoint and API key; request output is raw JSON from the configured QuoteNode/dataTrack endpoint.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
