## Description: <br>
Broadcasts an already signed transaction hex to a blockchain through the OKX Web3 API without requiring a private key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangchengming666](https://clawhub.ai/user/wangchengming666) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill when they already have a signed transaction and need an agent to validate inputs, call the OKX broadcast API, and return the resulting order ID, transaction hash, or error details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broadcasting a signed transaction is an irreversible financial action once accepted on chain. <br>
Mitigation: Verify the transaction contents, target chain, sender address, and MEV setting before running the broadcast. <br>
Risk: OKX Web3 API credentials are required and could be exposed through logs, shell history, or repositories if handled carelessly. <br>
Mitigation: Keep credentials out of logs and version control, and use least-privilege OKX Web3 API credentials. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangchengming666/broadcast-signed-transaction) <br>
- [OKX Web3 API](https://web3.okx.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns success status, order ID, transaction hash, explorer URL, MEV setting, and error details when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
