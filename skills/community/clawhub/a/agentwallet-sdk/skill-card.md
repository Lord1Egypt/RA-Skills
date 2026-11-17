## Description:

Non-custodial wallet SDK guidance for autonomous AI agents that need x402 payments, CCTP V2 bridge transfers, ERC-8004 identity, and Uniswap V3 swaps without custodial key handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[up2itnow](https://clawhub.ai/user/up2itnow)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to integrate non-custodial wallet operations into AI agents, including x402 API payments, token transfers, cross-chain USDC bridges, token swaps, and on-chain identity workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents using this skill may initiate transfers, swaps, bridges, x402 payments, or identity registration with financial impact.

Mitigation: Require explicit approval for transaction-producing actions and configure spend limits plus destination, chain, token, and payable-domain allowlists.

Risk: Wallet runtime compromise or dependency drift could expose funds or broaden agent authority.

Mitigation: Use pinned and reviewed package versions with a lockfile, isolate the wallet runtime, and operate with low-balance wallets or narrowly scoped session keys.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/up2itnow/skills/agentwallet-sdk)
- [agentwallet-sdk npm package](https://www.npmjs.com/package/agentwallet-sdk)
- [@agent-wallet/mastra-plugin npm package](https://www.npmjs.com/package/@agent-wallet/mastra-plugin)
- [clawpay-mcp npm package](https://www.npmjs.com/package/clawpay-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with TypeScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes npm package names, SDK usage examples, wallet operation guidance, and security considerations.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
