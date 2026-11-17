## Description:

Crypto market data from AiCoin Open API v3 across prices, K-lines, derivatives, news, signals, airdrops, treasuries, indices, and related market endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[procaross](https://clawhub.ai/user/procaross)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to retrieve current cryptocurrency market data and related AiCoin Open API v3 analytics through a Node.js command interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials may be stored in plaintext workspace .env files.

Mitigation: Prefer host-managed or scoped secret injection and avoid using set-key in shared workspaces.

Risk: The skill can access broad AiCoin analytics endpoints beyond basic market lookups.

Mitigation: Review endpoint usage before installation and limit credentials to the minimum AiCoin plan or permissions needed.

Risk: Market data and analytics may be unavailable, delayed, quota-limited, or gated by AiCoin plan permissions.

Mitigation: Check the ok and error fields in the returned JSON envelope and present failures or empty data without inventing values.

## Reference(s):

- [AiCoin Open Data](https://www.aicoin.com/opendata)
- [ClawHub skill page](https://clawhub.ai/procaross/skills/aicoin-market)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API response envelopes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command output uses a JSON envelope with ok, data, error, and meta fields.]

## Skill Version(s):

4.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
