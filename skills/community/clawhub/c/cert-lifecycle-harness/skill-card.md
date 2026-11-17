## Description:

Guides agents through human-controlled X.509/TLS certificate renewal, replacement, migration, auditing, and hardening workflows for complex infrastructure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dimayip](https://clawhub.ai/user/dimayip)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, security reviewers, and operations teams use this skill to plan, review, and execute certificate lifecycle changes with bounded human approvals, layered review artifacts, rollback planning, and strict controls around production writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable install or update paths can pull unreviewed code into an agent environment.

Mitigation: Install only from a pinned, reviewed release or commit and verify the release before use.

Risk: Production certificate runbook templates may affect live TLS traffic, secrets, Kubernetes resources, JKS stores, or sudo-managed files.

Mitigation: Require human security review of generated production scripts, secret handling, rollback behavior, deletion steps, sudo commands, and Kubernetes/JKS templates before execution.

Risk: Agent-assisted write operations can modify certificate bindings or infrastructure if gates are skipped.

Mitigation: Enforce the skill's six-gate process, use dry-run or canary execution for Import/Modify actions, and never delegate Delete operations to the agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dimayip/skills/cert-lifecycle-harness)
- [Agent Skills Specification](https://agentskills.io)
- [Certificate chain verification](artifact/references/cert-chain-verification.md)
- [Cloud API naming differences](artifact/references/cloud-api-naming.md)
- [SAN closure discovery](artifact/references/san-closure-discovery.md)
- [Topology detection](artifact/references/topology-detection.md)
- [Wildcard inventory](artifact/references/wildcard-inventory.md)
- [Phase 0 intake checklist](artifact/phases/00-intake-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documents with shell scripts, command blocks, checklists, runbooks, and configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces standalone review documents, scripts, runbooks, ADRs, inventories, and rollback materials for human review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
