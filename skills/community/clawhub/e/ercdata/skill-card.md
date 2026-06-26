## Description: <br>
Store, verify, and manage AI data on the Ethereum blockchain (Base network) using the ERCData standard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xReisearch](https://clawhub.ai/user/0xReisearch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and agents use ERCData to store data fingerprints, verify data integrity, create audit trails, manage access control for private data, and interact with the ERCData smart contract on Base mainnet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write commands submit real Base mainnet transactions and require access to a wallet key. <br>
Mitigation: Use a dedicated, minimally funded wallet; verify the contract and RPC endpoint before writes; and manually approve store, verify, access, and snapshot actions. <br>
Risk: Raw secrets or sensitive data stored on-chain or included in transaction calldata may be exposed. <br>
Mitigation: Store hashes or client-side encrypted data instead of raw secrets. <br>


## Reference(s): <br>
- [ERCData API Reference](references/api.md) <br>
- [ClawHub ERCData Skill Page](https://clawhub.ai/0xReisearch/ercdata) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, environment variables, and CLI arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Base mainnet read and write operations that require user-supplied wallet credentials and contract configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
