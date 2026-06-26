## Description: <br>
Query wallet balances, addresses, and UTxOs on the Cardano blockchain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adacapo21](https://clawhub.ai/user/adacapo21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to inspect a Cardano wallet's ADA balance, native token balances, addresses, and UTxOs through the configured MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a full Cardano wallet seed phrase for the configured wallet server, which can create wallet-compromise risk if exposed or used with an untrusted runtime. <br>
Mitigation: Use a watch-only setup or a dedicated low-value wallet when possible, audit and pin the MCP package before use, and keep the seed phrase out of prompts, logs, and project files. <br>
Risk: Wallet balances, addresses, and UTxOs may reveal sensitive financial information. <br>
Mitigation: Require explicit confirmation before displaying or using wallet data, and avoid sharing returned wallet details in untrusted contexts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/adacapo21/cardano-balances) <br>
- [Wallet Balances Concepts](references/concepts.md) <br>
- [Balances MCP Tools Reference](references/mcp-tools.md) <br>
- [Check Wallet Balances](sub-skills/check-balances.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown balance summary with converted ADA values and native asset lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet addresses and UTxO identifiers returned by the MCP server.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
