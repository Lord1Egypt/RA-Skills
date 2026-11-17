## Description:

Element Market API integration for querying NFT collection statistics, wallet portfolios, received offers, and recent NFT trading activity with an ELEMENT_API_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beelzebub520](https://clawhub.ai/user/beelzebub520)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent retrieve Element Market NFT collection metrics, rankings, wallet asset lists, received offers, and recent sale activity. It is suited to read-only market lookup and monitoring workflows that require an Element Market API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an Element Market API key.

Mitigation: Provide ELEMENT_API_KEY only through the agent environment and avoid exposing the key in prompts, logs, or shared command output.

Risk: Wallet lookups can reveal portfolio, offer, and trading activity to the Element Market API.

Mitigation: Ask for explicit positive confirmation before any wallet-address query and run only the specific lookup the user approved.

Risk: NFT price outputs can be misleading if payment token symbols or decimals are interpreted incorrectly.

Mitigation: Use the skill's token mapping table for supported chains and clearly flag unknown payment tokens rather than assuming a precise formatted price.

## Reference(s):

- [Element NFT Tracker Homepage](https://github.com/beelzebub520/element-nft-tracker)
- [Element API Documentation](https://element.readme.io/reference/api-overview)
- [Element API Key Page](https://element.market/apikeys)
- [Element Market](https://element.market)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and jq command snippets plus JSON-shaped API summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ELEMENT_API_KEY plus curl and jq; wallet lookups require explicit user consent.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
