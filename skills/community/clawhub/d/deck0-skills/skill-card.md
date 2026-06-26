## Description: <br>
Interact with DECK-0 digital collectibles platform to browse collections, buy card packs, open packs, view leaderboards, and apply as a publisher. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SignorCrypto](https://clawhub.ai/user/SignorCrypto) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an agent browse DECK-0 collections, buy and open digital card packs, inspect collection progress, view leaderboards, and submit publisher applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Buy and open flows execute real wallet transactions. <br>
Mitigation: Require explicit user confirmation before any buy, open, or publisher-submission action, and present transaction details before signing. <br>
Risk: Fallback signing can expose a sensitive private key through DECK0_PRIVATE_KEY. <br>
Mitigation: Prefer runtime wallet approval prompts; if fallback signing is needed, use a low-balance wallet and never print, log, or echo the private key. <br>
Risk: Purchases require native tokens and may fail or spend funds unexpectedly if chain, quantity, or price data is wrong. <br>
Mitigation: Confirm collection address, chain, quantity, payment amount, gas requirements, and signed price freshness before submitting the transaction. <br>


## Reference(s): <br>
- [DECK-0 app](https://app.deck-0.com) <br>
- [DECK-0 Skill page](https://clawhub.ai/SignorCrypto/deck0-skills) <br>
- [Agent Skills standard](https://skills.sh/) <br>
- [Foundry installation](https://book.getfoundry.sh/getting-started/installation) <br>
- [Apechain explorer](https://apescan.io) <br>
- [Base explorer](https://basescan.org) <br>
- [Authentication guide](auth.md) <br>
- [API endpoint reference](endpoints.md) <br>
- [Smart contract operations](smart-contracts.md) <br>
- [Workflow examples](examples.md) <br>
- [Error reference](errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown with inline JSON, shell commands, API request examples, and user-facing links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include DECK-0 share URLs, card URLs, transaction hashes, API response summaries, and wallet-action confirmations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
