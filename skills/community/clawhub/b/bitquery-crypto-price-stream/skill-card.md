## Description: <br>
Streams live Bitcoin price data from the Bitquery GraphQL WebSocket API, including OHLC ticks, USD volume, moving averages, and tick-to-tick percentage changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Divyn](https://clawhub.ai/user/Divyn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, traders, developers, and dashboard builders can use this skill to connect an agent to a live Bitcoin price stream and present current market ticks with basic derived metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Bitquery API key is passed in the WebSocket URL and can appear in logs, monitoring tools, or command history. <br>
Mitigation: Keep BITQUERY_API_KEY in a secure environment variable, avoid logging full WebSocket URLs, and rotate the key if it may have been exposed. <br>
Risk: The skill opens a live external WebSocket connection and depends on a third-party market data service. <br>
Mitigation: Run it first in a sandbox or virtual environment and install it only when live Bitquery Bitcoin streaming is intended. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/Divyn/bitquery-crypto-price-stream) <br>
- [Bitquery Trading.Tokens GraphQL field reference](references/graphql-fields.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples plus formatted live tick text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BITQUERY_API_KEY and network access to Bitquery's WebSocket API.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
