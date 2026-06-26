## Description: <br>
AuthLock provides MFA-bound local secret protection using TOTP-based encryption for passwords, certificates, keys, and other sensitive data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnluicn](https://clawhub.ai/user/johnluicn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use authlock to seal local secrets into .authlock vault locations and require a fresh TOTP code before decryption for workflows such as SSH keys, passwords, API tokens, and certificates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The vault stores the TOTP seed locally, so compromise of the .authlock directory can weaken the MFA-bound security model. <br>
Mitigation: Protect and back up the .authlock directory carefully, restrict local filesystem access, and avoid storing critical production credentials unless the local-seed model is acceptable. <br>
Risk: Decryption can send plaintext to stdout or files where an agent, shell history, logs, or chat transcript could expose it. <br>
Mitigation: Require a fresh TOTP code for each decryption, avoid echoing decrypted content, and write plaintext only to explicit user-approved paths or in-memory operations. <br>
Risk: The --exec path can provide decrypted credentials to arbitrary shell commands. <br>
Mitigation: Use --exec only with commands the user wrote and trusts, and avoid passing decrypted material to untrusted command strings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johnluicn/authlock) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local .authlock configuration and .sealed files; decryption can emit plaintext to stdout, a file, or a trusted execution command.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
