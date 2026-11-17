## Description:

Reliable Bitcoin Price Feed streams live Bitcoin OHLC ticks, USD volume, and moving-average metrics from the Bitquery GraphQL WebSocket API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[divyn](https://clawhub.ai/user/divyn)

### License/Terms of Use:

MIT-0

## Use Case:

Traders, developers, and analysts use this skill to subscribe to a live Bitcoin price stream and present OHLC ticks, USD volume, moving averages, and tick-to-tick percentage changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Bitquery API key is passed in the WebSocket URL and may be exposed through logs, shell history, or debugging output.

Mitigation: Use a dedicated low-privilege token, keep client and WebSocket debug logging off, avoid printing the full URL, and rotate the token if exposure is suspected.

Risk: The skill opens an outbound WebSocket connection and depends on the external Bitquery service and the gql websockets package.

Mitigation: Run the skill in a virtual environment or sandbox, allow only the required outbound endpoint, and prefer pinned dependencies or a lockfile before production use.

## Reference(s):

- [Reliable Bitcoin Price Feed on ClawHub](https://clawhub.ai/divyn/skills/bitquery-crypto-price-stream)
- [Bitquery Trading.Tokens GraphQL field reference](artifact/references/graphql-fields.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python examples, and streamed plain-text market ticks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BITQUERY_API_KEY and outbound WebSocket access to Bitquery; streamed values continue until interrupted or a timeout is supplied.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
