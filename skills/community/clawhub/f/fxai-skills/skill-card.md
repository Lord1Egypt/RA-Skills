## Description:

FXAI helps an agent create V5 tokens with optional USDT or BNB pools and prepare USDT/BNB buy and sell transactions through BNB Chain MCP using a configured private key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nathanthoreaurl](https://clawhub.ai/user/nathanthoreaurl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and crypto operators use FXAI to configure BNB Chain MCP, create V5 tokens with BNB or USDT pool settings, and prepare token buy or sell contract interactions. The skill is intended for workflows where the user understands wallet custody, token approvals, and irreversible on-chain transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide irreversible BNB Chain token creation and trading transactions using a configured PRIVATE_KEY.

Mitigation: Use a dedicated low-value wallet, verify contract addresses, token addresses, amounts, and allowances before signing, and review every transaction in the wallet or MCP flow.

Risk: The release uses unpinned install commands for MCP and skill tooling.

Mitigation: Prefer pinned and reviewed versions of the MCP server, skill package, and npm dependencies, and avoid global installation unless required.

Risk: The metadata upload helper sends a local image and token metadata to the Flap upload API.

Mitigation: Upload only public, non-sensitive images and metadata, and confirm the destination service is acceptable before using the helper script.

## Reference(s):

- [FXAI ClawHub Skill Page](https://clawhub.ai/nathanthoreaurl/skills/fxai-skills)
- [FXAI Contract ABI](references/contract-abi.md)
- [BNB Chain MCP Skills](https://docs.bnbchain.org/showcase/mcp/skills/)
- [Flap Token Launcher Guide](https://docs.flap.sh/flap/developers/token-launcher-developers/launch-token-through-portal)
- [Flap Deployed Contract Addresses](https://docs.flap.sh/flap/developers/token-launcher-developers/deployed-contract-addresses)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown instructions with shell commands and JSON-like contract call parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes contract addresses, ABI references, token approval steps, transaction call arguments, and local helper-script commands.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter and package metadata report 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
