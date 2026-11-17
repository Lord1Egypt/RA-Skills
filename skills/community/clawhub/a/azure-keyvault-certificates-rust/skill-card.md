## Description:

Azure Key Vault Certificates SDK for Rust guidance for creating, importing, and managing certificates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dsqsky](https://clawhub.ai/user/dsqsky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate Rust guidance, code snippets, and setup steps for Azure Key Vault certificate lifecycle operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Import and delete examples can affect sensitive certificate material or remove certificates from a target Key Vault.

Mitigation: Verify the target vault, certificate name, private-key handling, and Key Vault soft-delete and recovery settings before using those examples.

## Reference(s):

- [Acceptance Criteria](references/acceptance-criteria.md)
- [Azure Key Vault Certificates Rust API Reference](https://docs.rs/azure_security_keyvault_certificates)
- [Azure SDK for Rust Key Vault Certificates Source](https://github.com/Azure/azure-sdk-for-rust/tree/main/sdk/keyvault/azure_security_keyvault_certificates)
- [azure_security_keyvault_certificates crate](https://crates.io/crates/azure_security_keyvault_certificates)
- [ClawHub skill page](https://clawhub.ai/dsqsky/skills/azure-keyvault-certificates-rust)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Rust, shell, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Azure Key Vault certificate names, vault URLs, RBAC role guidance, and lifecycle operation examples.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
