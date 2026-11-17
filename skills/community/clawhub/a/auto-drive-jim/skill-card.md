## Description:

Upload and download files to Autonomys Network permanent decentralized storage through Auto-Drive, and save linked-list memory chains that can rebuild agent context from a CID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jim-counter](https://clawhub.ai/user/jim-counter)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to store and retrieve files on Auto-Drive and to save or recall permanent memory-chain entries for agent context reconstruction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded files and saved memories are public and permanent by default.

Mitigation: Do not upload secrets, private keys, confidential files, personal data, or full conversation context unless it is intentionally public or encrypted first.

Risk: AUTO_DRIVE_API_KEY exposure can affect the user's Auto-Drive account.

Mitigation: Prefer environment variables or a secret manager, avoid passing the key on the command line, and rotate the key if exposed.

Risk: Memory-chain recovery depends on retaining the latest CID.

Mitigation: Back up the lastCid value or anchor the latest CID with an external registry before relying on resurrection.

## Reference(s):

- [Auto-Drive API Reference](references/autodrive-api.md)
- [Autonomys Network Overview](references/autonomys-network.md)
- [Memory Chain & Resurrection Pattern](references/memory-chain.md)
- [Auto-Drive Dashboard](https://ai3.storage)
- [Auto-Drive API Docs](https://mainnet.auto-drive.autonomys.xyz/api/docs)
- [Autonomys Auto SDK](https://github.com/autonomys/auto-sdk)
- [Autonomys Auto-Drive](https://github.com/autonomys/auto-drive)
- [Autonomys Agents Framework](https://github.com/autonomys/autonomys-agents)
- [OpenClaw Memory Chain](https://github.com/autojeremy/openclaw-memory-chain)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Files, JSON, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, file, and AUTO_DRIVE_API_KEY for upload, memory-save, and chain-recall operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
