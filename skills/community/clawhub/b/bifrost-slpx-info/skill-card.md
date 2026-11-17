## Description:

Query Bifrost SLPx liquid staking protocol data on Ethereum, Base, Optimism, and Arbitrum, including vETH/ETH exchange rates, APY, TVL, user balances, redemption queue status, and protocol stats via read-only on-chain ERC-4626 calls and the Bifrost REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ark930](https://clawhub.ai/user/ark930)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and DeFi analysts use this skill to retrieve Bifrost vETH staking rates, yield, protocol statistics, wallet balances, and withdrawal queue status without signing transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses may be sent to Bifrost or public RPC endpoints during balance and withdrawal lookups.

Mitigation: Query only addresses the user is comfortable exposing to those endpoints.

Risk: Claimable-ETH results are informational and do not authorize or execute redemptions.

Mitigation: Use a trusted wallet or the official Bifrost app for any transaction and never provide private keys, seed phrases, or signing permissions to the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ark930/skills/bifrost-slpx-info)
- [Bifrost vETH page](https://www.bifrost.io/vtoken/veth)
- [Bifrost vETH app](https://app.bifrost.io/vstaking/vETH)
- [Bifrost site API](https://api.bifrost.app/api/site)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with optional shell command examples and decoded numeric results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fresh read-only API and RPC query results; no transaction signing or persistence.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
