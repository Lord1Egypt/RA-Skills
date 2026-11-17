## Description:

Installs a local OpenClaw multi-agent control-plane blueprint with per-agent workspaces, task lifecycle files, mailbox messaging tools, shared memory policy, and operational checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[delibrately-cmyk](https://clawhub.ai/user/delibrately-cmyk)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to bootstrap a local Team Lead plus specialist-agent workflow with structured task handoffs, mailbox messages, review states, and rollout checks. It is best treated as an operational blueprint that requires independent security controls before production reliance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included control-plane tools do not reliably enforce the isolation, approval, mailbox integrity, or audit controls described by the artifact.

Mitigation: Install only in an isolated test directory or account, and do not rely on it as a production security boundary until enforcement, authentication, permissions, logging, and integrity checks are added.

Risk: Agent messages and task transitions may be trusted more than the prototype tooling can justify.

Mitigation: Require human review of deployments, scan changes before use, and treat mailbox and task records as coordination aids rather than authoritative audit evidence.

## Reference(s):

- [Skill page](https://clawhub.ai/delibrately-cmyk/skills/cerberus-agent-foundry)
- [Protocol v1](assets/blueprint/docs/protocol-v1.md)
- [Operations Checklist](references/operations-checklist.md)
- [Shared Memory README](assets/blueprint/control-plane/shared-memory/README.md)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML configuration, Python scripts, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a filesystem blueprint that should be installed and tested in an isolated directory.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
