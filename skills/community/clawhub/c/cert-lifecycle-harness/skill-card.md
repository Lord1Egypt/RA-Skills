## Description: <br>
A certificate lifecycle harness that guides humans through X.509/TLS renewal, replacement, migration, inventory, review, dry-run, rollback, and verification workflows for complex infrastructure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dimayip](https://clawhub.ai/user/dimayip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, platform engineers, and security reviewers use this skill to plan and review certificate renewals, CA migrations, and TLS hardening work without handing final approval to the agent. It helps produce auditable runbooks, layered review artifacts, rollback plans, verification steps, and gated operational commands for certificate changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Templates may alter live certificate assets or production bindings. <br>
Mitigation: Require backups, dry-runs, explicit human approvals, rollback validation, and a reviewed maintenance window before any sudo, kubectl, service reload, or cloud write action. <br>
Risk: Delete or cleanup steps can be difficult to recover from, especially in certificate stores. <br>
Mitigation: Do not delegate Delete actions to the agent; remove or separately gate cleanup steps and keep destructive execution human-run. <br>
Risk: Certificate workflows often require sensitive cloud credentials, private keys, keystore passwords, or kubeconfig access. <br>
Mitigation: Do not paste long-lived credentials into chat; use user-run exports or short-lived least-privilege tokens scoped to the reviewed operation. <br>
Risk: The JKS rollover template deletes an alias before importing the replacement, which can leave the keystore empty if import fails. <br>
Mitigation: Validate the sequence in dry-run, confirm backups and restore commands, and require L1 review before using the template against production. <br>


## Reference(s): <br>
- [Skill specification](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Reference index](artifact/references/README.md) <br>
- [Cloud API naming guidance](artifact/references/cloud-api-naming.md) <br>
- [Certificate chain verification](artifact/references/cert-chain-verification.md) <br>
- [SAN closure discovery](artifact/references/san-closure-discovery.md) <br>
- [Dry-run matrix](artifact/phases/05-dry-run-matrix.md) <br>
- [Verify and rollback playbook](artifact/phases/06-verify-rollback-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with checklists, runbooks, review artifacts, and bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended to be reviewed by humans before production use; generated scripts and write actions require explicit approvals and dry-runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
