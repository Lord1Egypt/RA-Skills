## Description: <br>
Decanus Escrow provides an MCP server for onchain dual-deposit escrow between agents on Base L2, covering creation, acceptance, delivery proof, completion, disputes, refunds, and status checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manueltarouca](https://clawhub.ai/user/manueltarouca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to run Base Sepolia escrow workflows through MCP, including creating escrows, accepting contracts, submitting delivery proof, releasing funds, disputing terms, refunding expired escrows, and checking escrow state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP server can sign value-moving escrow transactions from the configured wallet. <br>
Mitigation: Use a dedicated low-balance Base Sepolia wallet and manually verify every escrow ID, address, amount, network, and transaction before approval. <br>
Risk: The required PRIVATE_KEY can expose wallet control if placed in shared configuration, logs, or primary wallets. <br>
Mitigation: Keep the private key out of shared files and logs, avoid production or primary keys, and rotate the wallet key if exposure is suspected. <br>
Risk: The skill starts an npm-distributed MCP package that can affect wallet signing behavior after install or update. <br>
Mitigation: Pin and review the @decanus-labs/escrow-mcp package before use or upgrade. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/manueltarouca/decanus-escrow) <br>
- [Escrow MCP homepage](https://github.com/decanus-labs/escrow-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with MCP tool names, parameter tables, bash commands, and YAML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write-tool responses can include transaction hashes and explorer URLs; read tools return escrow state, participants, amounts, deadlines, delivery hashes, and suggested next actions.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
