## Description: <br>
Look up labeled crypto addresses, token metadata, and balances across major EVM chains including Ethereum, Base, Arbitrum, Optimism, and BSC. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dawsbot](https://clawhub.ai/user/dawsbot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and blockchain analysts use this skill to identify labeled EVM addresses, search wallet labels, inspect token metadata, and check balances during crypto research or transaction review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses, labels, balance queries, and RPC endpoints may be shared with the configured MCP server, public API, or RPC provider. <br>
Mitigation: Use trusted endpoints, avoid submitting sensitive wallet research when privacy requirements prohibit third-party disclosure, and review MCP configuration before use. <br>
Risk: Installation relies on a referenced GitHub repository and npm dependencies. <br>
Mitigation: Install only from trusted sources and review dependency changes before running the MCP server. <br>


## Reference(s): <br>
- [Eth Labels Swagger docs](https://eth-labels.com/swagger) <br>
- [Eth Labels labeled accounts](https://eth-labels.com/accounts) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration snippets, and MCP lookup results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include address labels, token metadata, balances, chain IDs, and setup commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
