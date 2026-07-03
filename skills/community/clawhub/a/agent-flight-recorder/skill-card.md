## Description: <br>
Agent Flight Recorder creates an immutable, cryptographically verifiable audit trail for OpenClaw agent executions by registering SHA-256 file hashes, fetching Cryptowerk blockchain seals, and verifying proof sidecars. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cryptowerk-main](https://clawhub.ai/user/cryptowerk-main) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create proof-carrying audit artifacts for agent runs, decisions, and data files. It supports registering exact file hashes, retrieving seals, and verifying later proofs with local sidecar state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled or locally stored Cryptowerk credentials may be exposed if cwconfig.json is committed, backed up, or left broadly readable. <br>
Mitigation: Keep the skill directory out of watched source trees and backups, restrict permissions on cwconfig.json, and rotate credentials if the file is exposed. <br>
Risk: Registering or verifying a file sends its SHA-256 hash and proof data to Cryptowerk without an explicit confirmation step. <br>
Mitigation: Use the skill only for files whose hashes may be shared with Cryptowerk and require explicit approval before network registration or verification. <br>
Risk: .cwseal sidecars can contain retrieval IDs, seals, and verification history that may reveal workflow metadata. <br>
Mitigation: Store .cwseal files with the same access controls as the source data and avoid placing them in public or shared repositories. <br>


## Reference(s): <br>
- [Cryptowerk homepage](https://www.cryptowerk.com) <br>
- [Agent Flight Recorder on ClawHub](https://clawhub.ai/cryptowerk-main/agent-flight-recorder) <br>
- [Cryptowerk API Notes](references/cryptowerk-api-notes.md) <br>
- [Storage and State](references/storage-and-state.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline Python command examples and JSON sidecar artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local .cwseal sidecar files and cwconfig.json credential state.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
