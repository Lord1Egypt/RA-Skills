## Description: <br>
Stores agent decisions, identity, files, and context as permanent memory chains on the Autonomys Network so they can be recalled from a CID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jim-counter](https://clawhub.ai/user/jim-counter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to upload selected files or memory entries to Auto Drive, retrieve them by CID, and reconstruct an agent's memory chain after local state loss. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected memories or files may be uploaded to effectively permanent, public-by-default decentralized storage. <br>
Mitigation: Confirm the exact content before saving or uploading, and avoid secrets, private keys, tokens, regulated data, proprietary material, and personal information unless it has been minimized and protected. <br>
Risk: The AUTO_DRIVE_API_KEY and head CID can enable access to uploads or reconstruction of the memory chain. <br>
Mitigation: Treat the API key and head CID as sensitive values, store them securely, and share them only with trusted workflows. <br>
Risk: Recall operations can reintroduce old or unintended context into a new agent session. <br>
Mitigation: Review recalled memory-chain entries before relying on them for identity, decisions, or follow-up actions. <br>


## Reference(s): <br>
- [Auto Memory ClawHub page](https://clawhub.ai/jim-counter/auto-memory) <br>
- [Auto Drive API Reference](references/automemory-api.md) <br>
- [Autonomys Network Overview](references/autonomys-network.md) <br>
- [Memory Chain Reference](references/memory-chain.md) <br>
- [Auto Drive Dashboard](https://ai3.storage) <br>
- [Auto Drive API Docs](https://mainnet.auto-drive.autonomys.xyz/api/docs) <br>
- [Autonomys Auto Drive SDK](https://develop.autonomys.xyz/sdk/auto-drive/overview_setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce CIDs, gateway links, downloaded files, memory-chain JSON entries, and setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
