## Description: <br>
Azure Key Vault SDK for Python guidance for managing secrets, cryptographic keys, and certificates with secure storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thegovind](https://clawhub.ai/user/thegovind) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to configure and use Azure Key Vault Python SDK clients for secrets, keys, cryptographic operations, and certificates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Secret values or certificate private key material could be exposed if examples that retrieve or print sensitive values are copied into logs or shared output. <br>
Mitigation: Never print or log secret values or private keys; use managed identity or least-privilege credentials and keep sensitive values out of agent transcripts. <br>
Risk: Delete and purge examples can remove Azure Key Vault contents, including permanent deletion when purge is used. <br>
Mitigation: Require explicit human confirmation before delete or purge operations and test administrative flows against non-production vaults first. <br>
Risk: Examples that manage keys, certificates, or secrets may fail or overreach if run with broad or incorrect Azure permissions. <br>
Mitigation: Use scoped Azure RBAC roles and verify the target vault, key, secret, or certificate name before executing administrative commands. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes install commands, environment variable setup, client examples, error handling, and best-practice guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
