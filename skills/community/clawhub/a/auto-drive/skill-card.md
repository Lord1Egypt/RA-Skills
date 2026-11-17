## Description:

Indestructible agent memory: save files, decisions, identity, and context as permanent Auto-Drive CIDs and reconstruct linked memory chains from a single head CID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emilfattakhov](https://clawhub.ai/user/emilfattakhov)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to configure Auto-Drive access, upload and download files by CID, save permanent agent memories, and recall linked memory chains for state recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auto-Drive uploads are public and effectively permanent, so uploaded secrets or personal data may remain accessible.

Mitigation: Do not upload secrets, private keys, or sensitive personal data unless encrypted locally before upload.

Risk: Recalled memory chains can come from untrusted CIDs without proof of origin.

Mitigation: Only recall memory chains from CIDs the user trusts and inspect recalled JSON before importing it into agent memory.

Risk: API keys can be exposed through visible terminal input, command arguments, or logs.

Mitigation: Use environment or protected OpenClaw configuration storage for keys, avoid passing keys as command arguments, and rotate any exposed key.

## Reference(s):

- [Auto-Drive API Reference](artifact/references/autodrive-api.md)
- [Memory Chain & Resurrection Pattern](artifact/references/memory-chain.md)
- [Autonomys Network Overview](artifact/references/autonomys-network.md)
- [Auto-Drive Dashboard](https://ai3.storage)
- [Public Gateway](https://gateway.autonomys.xyz)
- [Auto-Drive API Docs](https://mainnet.auto-drive.autonomys.xyz/api/docs)
- [Auto-Drive SDK Docs](https://develop.autonomys.xyz/sdk/auto-drive/overview_setup)
- [Autonomys Auto SDK](https://github.com/autonomys/auto-sdk)
- [Autonomys Auto-Drive](https://github.com/autonomys/auto-drive)
- [ClawHub Skill Page](https://clawhub.ai/emilfattakhov/skills/auto-drive)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, files]

**Output Format:** [Markdown guidance with bash commands, CID strings, JSON memory results, and downloaded file content or paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, file, and AUTO_DRIVE_API_KEY for authenticated upload, memory save, and chain recall workflows.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
