## Description:

Plan Kubernetes cluster upgrades with API deprecation checks, addon compatibility verification, and rollback-safe runbooks

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to assess Kubernetes upgrade readiness, find deprecated API usage, review addon compatibility, and produce rollback-aware upgrade runbooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide privileged Kubernetes upgrade, drain, restart, backup, and rollback operations that may affect cluster availability.

Mitigation: Review every sudo, drain, upgrade, restart, and rollback command against the exact cluster and node before execution.

Risk: The artifact uses fixed /tmp paths for exported cluster state and API usage files.

Mitigation: Replace fixed /tmp paths with a private mktemp directory and restrictive permissions before running commands.

Risk: Backups and exported cluster state may contain sensitive operational data.

Mitigation: Protect or encrypt etcd snapshots and exported state, and restrict access to backup locations.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-reviewed upgrade plans, compatibility reports, deprecation findings, and rollback procedures.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
