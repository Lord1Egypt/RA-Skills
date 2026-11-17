## Description:

Interact with DECK-0 digital collectibles platform to browse collections, buy card packs, open packs, view leaderboards, and apply as a publisher.

This skill is ready for commercial/non-commercial use.

## Publisher:

[signorcrypto](https://clawhub.ai/user/signorcrypto)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to browse DECK-0 collections, manage packs and cards, purchase or open NFT packs on supported EVM networks, and apply to publish their own card collections through the DECK-0 API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide live blockchain transactions that spend native tokens.

Mitigation: Manually confirm the chain, contract address, pack IDs, quantity, total value, and gas before signing any transaction.

Risk: Fallback signing can use the sensitive DECK0_PRIVATE_KEY environment variable.

Mitigation: Prefer a runtime wallet, hardware wallet, or dedicated low-value wallet, and avoid DECK0_PRIVATE_KEY for real funds.

Risk: DECK-0 wallet-linked features can disclose wallet addresses, signatures, collection activity, recap data, and publisher application content to app.deck-0.com.

Mitigation: Install and use the skill only when those wallet-linked data flows match the user's intent.

## Reference(s):

- [DECK-0 ClawHub Skill](https://clawhub.ai/signorcrypto/skills/deck0-skills)
- [DECK-0 App](https://app.deck-0.com)
- [DECK-0 Agents OpenAPI](https://app.deck-0.com/api/agents/v1/openapi)
- [Foundry Installation](https://book.getfoundry.sh/getting-started/installation)
- [Agent Skills Standard](https://skills.sh/)
- [Apechain Explorer](https://apescan.io)
- [Base Explorer](https://basescan.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with API schemas, JSON examples, shell commands, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes authenticated API flows and on-chain transaction guidance; users should confirm transaction details before signing or spending funds.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
