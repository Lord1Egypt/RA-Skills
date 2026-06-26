## Description: <br>
Operate Chainbase indexed wallet and token reads through UXC with a curated OpenAPI schema, API-key auth, and read-first guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure UXC authentication and run read-only Chainbase Web3 API queries for wallet balances, token data, transaction history, token prices, and transaction details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried wallet addresses, token contract addresses, and transaction hashes are sent to Chainbase under the user's API key. <br>
Mitigation: Use a dedicated Chainbase API key where practical, rotate it when needed, and avoid submitting sensitive identifiers unless the data sharing is acceptable. <br>
Risk: The skill references a mutable GitHub main-branch URL for the OpenAPI schema. <br>
Mitigation: Use the bundled schema or a pinned schema URL when repeatability or change control matters. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Curated OpenAPI Schema](references/chainbase-web3.openapi.json) <br>
- [Chainbase API Key Authentication](https://docs.chainbase.com/quickstart/authenticate-your-api-key) <br>
- [Chainbase Web3 API Documentation](https://docs.chainbase.com/api-reference/web3-api/balance) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with inline bash commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only operations; queried wallet addresses, token contract addresses, and transaction hashes are sent to Chainbase under the user's API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
