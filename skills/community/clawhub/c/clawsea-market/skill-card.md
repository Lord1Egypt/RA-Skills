## Description: <br>
Non-custodial automation skill for ClawSea NFT marketplace. Use when an OpenClaw agent needs to browse collections, inspect NFTs/listings, and optionally execute non-custodial list, buy, and cancel flows through ClawSea and Seaport. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fluxmira-moltbot](https://clawhub.ai/user/fluxmira-moltbot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to let an OpenClaw agent browse ClawSea collections, inspect NFTs and listings, and optionally prepare or execute non-custodial marketplace actions with explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous signing or trading can move funds or alter marketplace state. <br>
Mitigation: Use read-only browsing without secrets by default; enable trading only with explicit approval, decoded transaction details, and an external signer or low-balance dedicated bot wallet. <br>
Risk: Wallet secrets could be exposed if pasted into chat, logged, or stored insecurely. <br>
Mitigation: Never request seed phrases or private keys in chat; keep any bot wallet key in a secure secret store and avoid printing, logging, or persisting it. <br>
Risk: Listings or ownership data can be stale or conflict with onchain state. <br>
Mitigation: Verify ownership and transaction preflights onchain before value-moving actions, and treat cancelled or reverted orders as stale. <br>
Risk: Unknown calldata or third-party transaction payloads may be unsafe. <br>
Mitigation: Require clear decoding and explicit user approval before executing transaction data from untrusted inputs. <br>


## Reference(s): <br>
- [ClawSea skill listing](https://clawhub.ai/fluxmira-moltbot/clawsea-market) <br>
- [ClawSea marketplace](https://clawsea.io) <br>
- [Publisher profile](https://clawhub.ai/user/fluxmira-moltbot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API routes, environment variable names, and safety checks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only browsing requires no secrets; autonomous trading requires a signer and explicit confirmation before value-moving actions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
