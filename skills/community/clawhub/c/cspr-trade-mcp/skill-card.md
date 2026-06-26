## Description: <br>
Trade on CSPR.trade DEX (Casper Network) for swaps, liquidity, and portfolio queries via the cspr-trade MCP server, with non-custodial transactions built remotely and signed locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mssteuer](https://clawhub.ai/user/mssteuer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect CSPR.trade market data, prepare swaps or liquidity actions, review portfolio positions, and follow user-confirmed signing and submission flows on Casper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading and liquidity operations can affect real funds. <br>
Mitigation: Verify token amounts, slippage, network, gas, transaction details, and expected outputs before approving; start on testnet or with small amounts. <br>
Risk: Private keys or mnemonics could be exposed if a user shares them in chat or misconfigures signing. <br>
Mitigation: Never paste private keys or mnemonics into chat; configure any local signer yourself and only with a wallet you are comfortable using. <br>
Risk: A transaction could be signed or submitted before the user fully reviews it. <br>
Mitigation: Require explicit user confirmation before signing or submitting, and present unsigned transaction details before each signing step. <br>


## Reference(s): <br>
- [CSPR.trade MCP homepage](https://mcp.cspr.trade) <br>
- [CSPR.trade MCP source repository](https://github.com/make-software/cspr-trade-mcp) <br>
- [ClawHub release page](https://clawhub.ai/mssteuer/cspr-trade-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, JSON configuration snippets, transaction summaries, and MCP tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include unsigned or signed transaction JSON summaries and transaction hashes when user-controlled MCP tools are available.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
