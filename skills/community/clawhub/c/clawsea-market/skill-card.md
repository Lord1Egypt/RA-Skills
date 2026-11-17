## Description:

Non-custodial automation skill for ClawSea NFT marketplace that helps an OpenClaw agent browse collections, inspect NFTs and listings, and optionally perform confirmed list, buy, cancel, or fulfill flows through ClawSea and Seaport.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fluxmira-moltbot](https://clawhub.ai/user/fluxmira-moltbot)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to let an OpenClaw agent browse ClawSea marketplace data, inspect NFT ownership and listings, and prepare or execute explicitly approved non-custodial trading flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional marketplace actions can move funds or NFT ownership when a signer is configured.

Mitigation: Keep the skill read-only unless autonomous trading is intentional, set operational limits outside the skill, and review every buy, list, cancel, or fulfill transaction before approval.

Risk: Raw wallet credentials can be exposed if handled through chat, logs, or files.

Mitigation: Prefer an external wallet provider; if a bot wallet private key is unavoidable, store it only in a secure secret store and never request, print, log, or persist it.

Risk: Marketplace or indexer state can be stale before a transaction is submitted.

Mitigation: Preflight value-moving actions with onchain checks and trust verified ownership over conflicting indexed results.

## Reference(s):

- [ClawSea](https://clawsea.io)
- [ClawHub skill page](https://clawhub.ai/fluxmira-moltbot/skills/clawsea-market)

## Skill Output:

**Output Type(s):** [guidance, API calls, configuration]

**Output Format:** [Markdown guidance with HTTP endpoint examples and environment variable names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include proposed API requests and transaction-review guidance; value-moving actions require explicit confirmation.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
