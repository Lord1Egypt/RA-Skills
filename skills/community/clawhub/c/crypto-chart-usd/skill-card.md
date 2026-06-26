## Description: <br>
Streams real-time multi-token, multi-chain crypto chart data with 1-second OHLC ticks, USD volume, and USD pricing from the Bitquery Trading.Tokens API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[divyn](https://clawhub.ai/user/divyn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to connect an agent or local script to Bitquery's live WebSocket feed for crypto dashboards, charting, and token monitoring across supported chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required Bitquery API key is embedded in the WebSocket URL, which can expose the key through logs, shell history, debugging tools, or network monitoring. <br>
Mitigation: Use a dedicated or revocable key, provide it only through a secure environment variable, avoid logging full WebSocket URLs, and rotate the key immediately if exposure is suspected. <br>
Risk: The skill opens a live external WebSocket connection and depends on third-party market data availability and behavior. <br>
Mitigation: Run it in an isolated environment first, confirm logging behavior before shared or production use, and treat streamed prices as external data that should be validated before operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/divyn/crypto-chart-usd) <br>
- [Bitquery Trading.Tokens GraphQL field reference](references/graphql-fields.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell commands; the runtime script streams formatted text ticks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BITQUERY_API_KEY and a WebSocket connection to Bitquery; stream output continues until stopped or a timeout is provided.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
