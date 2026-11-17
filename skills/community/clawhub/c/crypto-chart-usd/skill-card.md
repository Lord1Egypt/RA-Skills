## Description:

Streams real-time Bitquery Trading.Tokens data for multi-token, multi-chain crypto charting with 1-second OHLC ticks, USD volume, and USD pricing where available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[divyn](https://clawhub.ai/user/divyn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to stream live crypto market ticks into charting, monitoring, or dashboard workflows across supported chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Bitquery API token is passed in the WebSocket URL and can leak through logs, shell history, network tooling, or captured URLs.

Mitigation: Store the token only in a secure environment variable, avoid printing or logging full WebSocket URLs, run in an isolated environment, and rotate the token if exposure is suspected.

Risk: The skill depends on an unpinned Python package, which can change behavior across installs.

Mitigation: Use a virtual environment or container and pin dependencies before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/divyn/skills/crypto-chart-usd)
- [Bitquery Trading.Tokens GraphQL field reference](references/graphql-fields.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; runtime script prints formatted text ticks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BITQUERY_API_KEY and outbound WebSocket access to Bitquery.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
