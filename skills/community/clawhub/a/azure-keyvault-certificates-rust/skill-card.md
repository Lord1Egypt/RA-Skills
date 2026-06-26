## Description: <br>
Azure Key Vault Certificates SDK for Rust guidance for creating, importing, and managing certificates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dsqsky](https://clawhub.ai/user/dsqsky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate Rust guidance and code snippets for Azure Key Vault certificate client setup, certificate CRUD operations, policy management, RBAC setup, and lifecycle best practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated certificate-management examples can perform powerful actions against Azure Key Vault resources, including creating, updating, deleting, or purging certificates. <br>
Mitigation: Review the target vault URL, Azure tenant and subscription, signed-in account, RBAC role, and any delete or purge operation before running generated code. <br>
Risk: Examples that include certificate import passwords or certificate material can lead to accidental exposure if real secrets are hardcoded or committed. <br>
Mitigation: Use placeholders in generated examples, supply real secrets through approved secret-management channels, and avoid storing certificate passwords in source code. <br>
Risk: Overbroad certificate permissions can allow unintended certificate lifecycle changes. <br>
Mitigation: Prefer least-privilege Azure Key Vault roles and grant elevated roles such as Key Vault Certificates Officer only when the workflow requires them. <br>


## Reference(s): <br>
- [Azure Key Vault Certificates SDK for Rust acceptance criteria](references/acceptance-criteria.md) <br>
- [API Reference](https://docs.rs/azure_security_keyvault_certificates) <br>
- [Source Code](https://github.com/Azure/azure-sdk-for-rust/tree/main/sdk/keyvault/azure_security_keyvault_certificates) <br>
- [crates.io](https://crates.io/crates/azure_security_keyvault_certificates) <br>
- [ClawHub skill page](https://clawhub.ai/dsqsky/azure-keyvault-certificates-rust) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with Rust and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Examples may include Azure vault URLs, authentication setup, certificate names, certificate policy fields, RBAC roles, and delete or purge operations.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
