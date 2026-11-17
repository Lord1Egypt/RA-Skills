## Description:

Deep data migration workflow covering scope, mapping, validation, batching and ordering, dual-write and cutover, rollback, and reconciliation for tenant moves, bulk backfills, and store changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawkk](https://clawhub.ai/user/clawkk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan high-trust data migrations, including tenant moves, bulk backfills, schema-related data movement, and cutovers with minimal downtime. It guides mapping, batching, validation, rollback, and post-cutover reconciliation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using migration planning guidance without review can leave gaps in the runbook, rollback plan, validation checks, or PII and compliance handling.

Mitigation: Have a human review the runbook, rollback plan, validation checks, and PII or compliance requirements before using the guidance for a real migration.

Risk: Data migration work can fail through silent corruption, ordering bugs, or unclear cutover decisions.

Mitigation: Document invariants and mappings, use checkpoints and idempotent batches, run validation and shadow checks, test rollback, and complete post-cutover reconciliation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/clawkk/skills/data-move)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands]

**Output Format:** [Markdown guidance with checklists, runbook steps, validation criteria, and optional command or configuration suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not execute migrations; output should be reviewed before production use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
