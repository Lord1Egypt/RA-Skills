## Description: <br>
Autonomous state persistence engine that encrypts, secures, and anchors agent memories, state snapshots, and evolved skills onto 0G Storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[web3senior](https://clawhub.ai/user/web3senior) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to package, encrypt, upload, and later recover agent state from 0G Storage after resets, device changes, or local environment loss. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can package local state and send it to decentralized storage. <br>
Mitigation: Inspect the exact archive or file before upload and use encrypted upload for any private or operational state. <br>
Risk: Recovery depends on encryption keys that are not recoverable if lost. <br>
Mitigation: Store recovery keys in a real secret manager and avoid placing them in chat, MEMORY.md, shell history, logs, or tracking databases. <br>
Risk: Upload commands require wallet credentials. <br>
Mitigation: Use a dedicated low-value wallet and protect the private key outside the agent transcript and project files. <br>


## Reference(s): <br>
- [0G Storage reference](references/0g-storage.md) <br>
- [0G Storage Scan Tool](https://storagescan.0g.ai/tool) <br>
- [0G Storage Scan](https://storagescan.0g.ai/) <br>
- [0G ClawBack on ClawHub](https://clawhub.ai/web3senior/0g-clawback) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires 0G RPC and indexer configuration plus a wallet private key for upload commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
