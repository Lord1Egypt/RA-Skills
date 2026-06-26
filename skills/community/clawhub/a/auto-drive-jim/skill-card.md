## Description: <br>
Upload and download files to Autonomys Network permanent decentralized storage via Auto-Drive, and save memories as a linked-list chain for reconstructing agent context from a single CID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jim-counter](https://clawhub.ai/user/jim-counter) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to upload selected files or memory entries to Auto-Drive, retrieve files by CID, and reconstruct an agent memory chain from the latest stored CID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected files or memory notes can be uploaded to public, permanent Auto-Drive storage. <br>
Mitigation: Review, redact, or encrypt content before upload; do not upload secrets, credentials, private documents, personal data, or proprietary context unless that exposure is intentional. <br>
Risk: Recalled memory-chain content can affect future agent behavior. <br>
Mitigation: Review recalled chain content before allowing it to guide future agent actions. <br>


## Reference(s): <br>
- [Auto-Drive API Reference](references/autodrive-api.md) <br>
- [Memory Chain & Resurrection Pattern](references/memory-chain.md) <br>
- [Autonomys Network Overview](references/autonomys-network.md) <br>
- [Auto-Drive API Docs](https://mainnet.auto-drive.autonomys.xyz/api/docs) <br>
- [Auto-Drive Dashboard](https://ai3.storage) <br>
- [Autonomys Auto-Drive SDK Docs](https://develop.autonomys.xyz/sdk/auto-drive/overview_setup) <br>
- [Autonomys Auto SDK](https://github.com/autonomys/auto-sdk) <br>
- [Autonomys Auto-Drive](https://github.com/autonomys/auto-drive) <br>
- [Autonomys Agents Framework](https://github.com/autonomys/autonomys-agents) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Files, JSON, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; script outputs include CID strings, JSON records, and downloaded files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, file, and AUTO_DRIVE_API_KEY for uploads, memory saves, and authenticated chain recall.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
