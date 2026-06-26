## Description: <br>
Encrypt files, secure passwords, manage keys, and audit code for cryptographic best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to choose encryption patterns, hash passwords, manage keys, configure TLS, protect mobile storage, and audit code for cryptographic mistakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Infrastructure examples can alter certificates, secrets, Vault policies, deployments, or evidence files if run directly. <br>
Mitigation: Run snippets only in authorized environments after confirming the target, maintenance window, rollback plan, and secure handling of generated evidence. <br>
Risk: Cryptographic guidance may be misapplied to a system with different compliance, threat model, or platform constraints. <br>
Mitigation: Review algorithm choices, key lifecycle, storage, rotation, and audit requirements with security owners before production use. <br>


## Reference(s): <br>
- [Encryption skill page](https://clawhub.ai/ivangdavila/encryption) <br>
- [Encryption Code Patterns](artifact/patterns.md) <br>
- [Mobile Encryption Patterns](artifact/mobile.md) <br>
- [Infrastructure Encryption Patterns](artifact/infra.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides guidance snippets and audit checklists; generated commands should be reviewed before execution in target environments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
