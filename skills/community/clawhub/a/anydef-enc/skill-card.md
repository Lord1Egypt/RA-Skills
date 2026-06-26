## Description: <br>
Local-only agent data encryption toolkit with an MK->KEK->DEK hierarchy for browser-based OpenClaw data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anydefai](https://clawhub.ai/user/anydefai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agent operators use this skill to encrypt local agent memory, history, assets, and other scoped data with passphrase-derived keys while keeping encryption operations local. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the advertised key-rotation helper does not actually rotate keys. <br>
Mitigation: Do not rely on the rotation helper for incident response or passphrase compromise until key rotation is implemented and tested. <br>
Risk: Encrypted data is unrecoverable if the passphrase is lost. <br>
Mitigation: Maintain passphrase recovery procedures and backups before using the skill for important data. <br>
Risk: Storage confidentiality depends on how the OpenClaw environment implements window.storage. <br>
Mitigation: Confirm whether storage is local, synced, or shared before storing sensitive encrypted data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anydefai/anydef-enc) <br>
- [Local Encryption Architecture](references/full-implementation.md) <br>
- [Storage Keys Dictionary](references/storage-keys.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration, Guidance, Text] <br>
**Output Format:** [JavaScript module APIs and encrypted string payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses browser SubtleCrypto and window.storage; no required credentials are declared.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release evidence and metadata.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
