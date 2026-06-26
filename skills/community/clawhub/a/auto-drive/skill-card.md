## Description: <br>
Auto-Drive lets agents upload files, save permanent memory-chain entries, download CIDs, and rebuild history from Auto-Drive storage on the Autonomys Network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EmilFattakhov](https://clawhub.ai/user/EmilFattakhov) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent needs to store files or memory entries permanently, retrieve content by CID, or reconstruct a memory chain after local state loss. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploads and saved memories are permanent and public by default, so secrets, credentials, private keys, or sensitive personal data can be exposed indefinitely. <br>
Mitigation: Review each file or memory entry before upload and do not store secrets or sensitive personal data in Auto-Drive. <br>
Risk: The Auto-Drive API key authorizes uploads and account access for the configured user. <br>
Mitigation: Store AUTO_DRIVE_API_KEY only in the intended local configuration or environment, rotate it if exposed, and avoid printing it in logs or shared transcripts. <br>
Risk: Recalling a memory chain from an untrusted CID can import misleading or unwanted context into an agent session. <br>
Mitigation: Recall chains only from CIDs the user trusts and inspect reconstructed entries before using them as operational memory. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/EmilFattakhov/auto-drive) <br>
- [Auto-Drive API Reference](references/autodrive-api.md) <br>
- [Autonomys Network Overview](references/autonomys-network.md) <br>
- [Memory Chain & Resurrection Pattern](references/memory-chain.md) <br>
- [Auto-Drive Dashboard](https://ai3.storage) <br>
- [Auto-Drive API Docs](https://mainnet.auto-drive.autonomys.xyz/api/docs) <br>
- [Autonomys Auto SDK](https://github.com/autonomys/auto-sdk) <br>
- [Autonomys Auto-Drive](https://github.com/autonomys/auto-drive) <br>
- [Autonomys Agents](https://github.com/autonomys/autonomys-agents) <br>
- [OpenClaw memory-chain example](https://github.com/autojeremy/openclaw-memory-chain) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces CIDs, gateway links, downloaded files, memory-chain JSON entries, and local state updates when the scripts are run.] <br>

## Skill Version(s): <br>
1.0.4 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
