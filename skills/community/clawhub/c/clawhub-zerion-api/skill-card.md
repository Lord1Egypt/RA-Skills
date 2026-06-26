## Description: <br>
Access real-time crypto wallet portfolios, transactions, DeFi positions, token prices, NFTs, and gas fees across EVM chains and Solana via Zerion API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abishekdharshan](https://clawhub.ai/user/abishekdharshan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and research teams use this skill to query wallet portfolios, transaction history, DeFi positions, token prices, NFTs, gas fees, and cross-chain activity through Zerion's remote MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet address lookups and related query context can reveal sensitive financial behavior to Zerion's remote MCP service. <br>
Mitigation: Only query wallets with authorization and an appropriate legal or compliance basis, especially for customer-linked or personally linked wallets. <br>
Risk: The skill requires a Zerion API key for remote service access. <br>
Mitigation: Use a dedicated, least-privilege Zerion API key and avoid sharing it in prompts, logs, or generated output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abishekdharshan/clawhub-zerion-api) <br>
- [Zerion API documentation](https://developers.zerion.io) <br>
- [Zerion MCP and AI documentation](https://developers.zerion.io/reference/building-with-ai) <br>
- [Zerion llms.txt](https://developers.zerion.io/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with optional JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on Zerion API authentication, supported chains, and the wallet or token identifiers supplied by the user.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
