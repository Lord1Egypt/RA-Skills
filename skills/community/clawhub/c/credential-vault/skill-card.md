## Description: <br>
Credential Vault provides encrypted local credential storage for OpenClaw agents so API keys do not need to be kept in plaintext files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChloePark85](https://clawhub.ai/user/ChloePark85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to initialize and unlock a local credential vault, add and retrieve API keys, organize credentials with tags, export credentials into the environment, and review expiry and audit information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The unlocked session key is stored on disk, leaving powerful unlock material available until the vault is locked. <br>
Mitigation: Use only for local development unless the session-key design is fixed, run vault lock promptly, and avoid leaving sessions unlocked across reboots or shared machines. <br>
Risk: Credential export workflows can expose secrets as plaintext environment lines or shell output. <br>
Mitigation: Do not use eval on untrusted vault output, avoid echoing secrets, and do not write exported credentials to temporary or shared text files. <br>
Risk: The security evidence warns against relying on this as production or team secret management. <br>
Mitigation: Add protected session storage, strict file permissions, expiry enforcement, and safer export workflows before production or team use. <br>


## Reference(s): <br>
- [Credential Vault ClawHub page](https://clawhub.ai/ChloePark85/credential-vault) <br>
- [README](artifact/README.md) <br>
- [Usage examples](artifact/EXAMPLE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text] <br>
**Output Format:** [CLI text, Markdown guidance, bash commands, and KEY=VALUE environment lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local vault files, audit log entries, and environment exports when the user runs the provided commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
