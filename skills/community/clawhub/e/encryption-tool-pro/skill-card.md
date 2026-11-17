## Description:

Enterprise security teams use this skill for KMS and Vault integration, key rotation, compliance audits, batch file encryption, and deep cryptographic code scanning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, DevSecOps engineers, and enterprise security teams use this skill to prepare encryption workflows, compliance checks, security audit reports, and operational commands for projects that need stronger key-management practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent through high-impact read, write, and command-execution workflows with weak path scoping.

Mitigation: Review before installing, run only on explicitly selected paths, and verify proposed commands before execution.

Risk: The included envelope-encryption examples may be mistaken for production-grade protection.

Mitigation: Replace example key wrapping with a real KMS or Vault-backed implementation before production use.

Risk: Generated .meta files and audit reports may contain sensitive operational details.

Mitigation: Keep generated metadata and reports out of logs and source control unless they have been reviewed and sanitized.

Risk: Callback URLs can send workflow results to unintended destinations.

Mitigation: Use callbacks only when the destination is trusted and explicitly approved.

## Reference(s):

- [Detailed reference](references/detail.md)
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/encryption-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code, shell commands, YAML configuration, and structured status or report descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe generated report files, encrypted file metadata, audit outputs, and configuration changes depending on the requested workflow.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
