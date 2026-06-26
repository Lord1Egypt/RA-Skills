## Description: <br>
Arcadia Finance helps agents manage DeFi liquidity on Uniswap, Aerodrome, and Velodrome across Base, Unichain, and Optimism, including concentrated liquidity positions, automation, yield optimization, leverage, and single-sided lending liquidity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thomas-smets](https://clawhub.ai/user/thomas-smets) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and DeFi operators use this skill to inspect Arcadia accounts, pools, strategies, contracts, and automation options, then prepare unsigned transactions for wallet review and signing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DeFi write operations produce unsigned transactions that can move assets, grant approvals, enable automation, or introduce leverage once signed. <br>
Mitigation: Independently inspect every wallet prompt for chain, recipient contract, token, amount, approval scope, and leverage or automation effects before signing. <br>
Risk: Changing ARCADIA_MCP_URL can route wallet addresses and transaction parameters to a different endpoint. <br>
Mitigation: Use the default Arcadia endpoint unless intentionally testing another trusted server. <br>
Risk: Private keys, seed phrases, or wallet secrets would create severe custody risk if shared with an agent or remote endpoint. <br>
Mitigation: Never provide seed phrases or private keys; use only public addresses and separate wallet signing. <br>
Risk: Leveraged liquidity or automation settings can affect account health and liquidation risk. <br>
Mitigation: Check account health with read_account_info and confirm the intended strategy before preparing or signing risky transactions. <br>


## Reference(s): <br>
- [Arcadia Finance Website](https://arcadia.finance) <br>
- [Arcadia Finance Documentation](https://docs.arcadia.finance) <br>
- [Arcadia MCP Tool Documentation](https://mcp.arcadia.finance/llms-full.txt) <br>
- [ClawHub Skill Page](https://clawhub.ai/thomas-smets/arcadia-finance) <br>
- [Contract Addresses](contracts.md) <br>
- [Wallet Signing Guide](wallet-signing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON arguments; tool calls may return JSON-like text and unsigned transaction objects.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; write operations return unsigned transactions for separate wallet review, signing, and broadcast.] <br>

## Skill Version(s): <br>
1.1.3 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
