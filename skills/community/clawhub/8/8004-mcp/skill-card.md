## Description: <br>
Register and manage agent identity, reputation, and feedback on Solana and EVM chains using the multi-chain ERC-8004 Agent Registry protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MonteCrypto999](https://clawhub.ai/user/MonteCrypto999) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to search agent registries, inspect reputation and feedback, manage wallets, and perform ERC-8004 registration or feedback operations across Solana and EVM chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage wallet material and initiate blockchain write operations through an external MCP server. <br>
Mitigation: Use testnet first, use a dedicated low-balance wallet, keep secrets out of chat logs, and require explicit approval before wallet imports, transfers, feedback, registrations, URI updates, mainnet use, or other write operations. <br>
Risk: The external @quantulabs/8004-mcp package is installed or run through npm tooling. <br>
Mitigation: Install only if the package is trusted; pin and review the package where possible before deployment. <br>
Risk: Unnecessary environment variables may be exposed to the MCP server process. <br>
Mitigation: Pass only the environment variables required for the intended chain, network, and storage configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MonteCrypto999/8004-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/MonteCrypto999) <br>
- [README.md](artifact/README.md) <br>
- [Agent integration guide](artifact/skill.md) <br>
- [8004-solana SDK](https://github.com/QuantuLabs/8004-solana) <br>
- [agent0-ts SDK](https://github.com/agent0lab/agent0-ts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript, JavaScript, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke MCP tools that return registry data, wallet status, unsigned transactions, transaction hashes, and configuration details.] <br>

## Skill Version(s): <br>
0.2.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
