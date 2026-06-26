## Description: <br>
Backend Agent Data Encryption. High-security MK->KEK->DEK hierarchy for backend environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anydefai](https://clawhub.ai/user/anydefai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and backend agent operators use this skill to add local filesystem-backed encryption for Node.js agents, including multi-user and channel-isolated storage for memory, cache, logs, and assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weak or lost passphrases can make the local encryption vault either easier to attack or unrecoverable. <br>
Mitigation: Use strong passphrases, document recovery expectations, and protect passphrase handling outside the skill. <br>
Risk: The skill writes vault metadata and encrypted asset files under the working directory. <br>
Mitigation: Restrict filesystem permissions for the working directory and vault files before using the skill in shared backend environments. <br>
Risk: Unsanitized user, channel, scope, or asset key inputs can affect local storage paths or key names. <br>
Mitigation: Validate and sanitize context identifiers and asset keys before passing them to the encryption service. <br>


## Reference(s): <br>
- [Backend Storage Schema](references/storage-keys.md) <br>
- [ClawHub skill page](https://clawhub.ai/anydefai/backendenc) <br>


## Skill Output: <br>
**Output Type(s):** [code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript usage examples and local storage configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Node.js runtime with crypto and filesystem access; encrypted vault data is stored locally.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata and artifact metadata.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
