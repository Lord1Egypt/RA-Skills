## Description:

Provides agent guidance and shell commands for querying AiCoin Open API v3 Hyperliquid analytics, including whale positions, liquidations, open interest, trader statistics, taker flow, and funding data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[procaross](https://clawhub.ai/user/procaross)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, analysts, and agents use this skill to query AiCoin's Hyperliquid market and on-chain analytics, inspect whale activity, liquidations, trader performance, open interest, taker flow, and funding data, and summarize real API results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a networked AiCoin API tool that broadly handles local API credentials.

Mitigation: Use a dedicated low-privilege AiCoin key and keep unrelated secrets out of the working and OpenClaw .env files.

Risk: The skill can save an AiCoin API secret in plaintext .env files.

Mitigation: Store only the required AiCoin credential, restrict file access, and rotate the key if the workspace is shared or exposed.

Risk: The skill may call non-Hyperliquid AiCoin endpoints despite its Hyperliquid framing.

Mitigation: Review requested endpoint paths before execution and verify AICOIN_BASE_URL points only to the official AiCoin service.

## Reference(s):

- [AiCoin OpenData](https://www.aicoin.com/opendata)
- [ClawHub skill page](https://clawhub.ai/procaross/skills/aicoin-hyperliquid)
- [OpenClaw metadata source](https://github.com/aicoincom/coinos-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON command examples and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AiCoin API envelopes with ok, data, error, and meta fields.]

## Skill Version(s):

4.0.0 (source: package.json and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
