## Description: <br>
Query on-chain crypto data through the AVE Cloud API for token discovery, market data, holder analysis, transaction history, contract risk reports, and pro-plan real-time streams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hope-Ave](https://clawhub.ai/user/Hope-Ave) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to query AVE Cloud for on-chain token, DEX, holder, swap, trend, and contract-risk data, then summarize the returned JSON as readable tables or summaries. Pro-plan users can also monitor live price, swap, liquidity, and kline streams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an AVE Cloud API key and may pass that key into Docker environments for pro-mode streams. <br>
Mitigation: Use a scoped AVE Cloud key, avoid pro-mode Docker streams when not needed, and review the Docker behavior before running pro streams. <br>
Risk: Pro mode can manage a persistent Docker container for WebSocket streaming. <br>
Mitigation: Stop the ave-cloud-server container when streaming is finished and prefer the REST commands when persistent containers are unnecessary. <br>


## Reference(s): <br>
- [AVE Cloud skill page](https://clawhub.ai/Hope-Ave/ave-cloud) <br>
- [AVE Cloud](https://cloud.ave.ai/) <br>
- [AVE Cloud API Reference](https://ave-cloud.gitbook.io/data-api) <br>
- [API endpoints reference](references/api-endpoints.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands and JSON-derived tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AVE_API_KEY and API_PLAN; pro streams require API_PLAN=pro and Docker or local WebSocket dependencies.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
