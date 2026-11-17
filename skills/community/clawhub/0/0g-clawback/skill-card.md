## Description:

Autonomous state persistence engine that encrypts, secures, and anchors agent memories, state snapshots, and evolved skills onto 0G Storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[web3senior](https://clawhub.ai/user/web3senior)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to back up, encrypt, upload, download, and recover OpenClaw agent state through 0G Storage. It is intended for state checkpoints, recovery after local environment loss, and controlled persistence of agent memories or skill artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive agent state, wallet keys, and encryption keys, and the server security verdict is suspicious.

Mitigation: Review carefully before installation, use only a disposable low-value test wallet, and avoid backing up whole workspaces or MEMORY.md files without inspecting exactly what will be uploaded.

Risk: A committed .env file is present in the release artifact hash list.

Mitigation: Remove committed environment secrets and provide local configuration through a secret manager or deployment environment instead.

Risk: Encrypted uploads return encryptionKeyHex, and lost keys cannot be recovered.

Mitigation: Store encryption keys in a real secret manager, not agent memory, project notes, or public storage.

Risk: The release has no server-resolved GitHub import provenance.

Mitigation: Verify the canonical repository and package source manually before execution.

## Reference(s):

- [0G Storage Reference](references/0g-storage.md)
- [0G Storage Scan Tool](https://storagescan.0g.ai/tool)
- [0G Storage Scan](https://storagescan.0g.ai/)
- [0G Testnet RPC](https://evmrpc-testnet.0g.ai)
- [0G Storage Testnet Indexer](https://indexer-storage-testnet-turbo.0g.ai)
- [ClawHub Skill Page](https://clawhub.ai/web3senior/skills/0g-clawback)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may produce root hashes, transaction hashes, recovered file paths, and encryption key material for encrypted uploads.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
